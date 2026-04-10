from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.core.exceptions import ValidationError
import uuid
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings


class Usuario(AbstractUser):
    class Role(models.TextChoices):
        SINDICO = "SINDICO", "Síndico"
        PORTEIRO = "PORTEIRO", "Porteiro"
        MORADOR = "MORADOR", "Morador"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MORADOR)
    casa_bloco = models.CharField("Unidade/Casa", max_length=10, blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"
    

class ReservaSalao(models.Model):
    # Troque 'User' por settings.AUTH_USER_MODEL
    morador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data = models.DateField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Verifica se já existe reserva para esta data
        if ReservaSalao.objects.filter(data=self.data).exists():
            raise ValidationError(f"Lamento! O Salão de Festas já está reservado para o dia {self.data.strftime('%d/%m/%Y')}.")

    def __str__(self):
        return f"Salão - {self.data} - {self.morador.username}"

class Veiculo(models.Model):
    TIPOS = [
    ('CARRO', '🚗 Carro'),
    ('MOTO', '🏍️ Moto'),
 ]
    morador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPOS, default='CARRO')
    placa = models.CharField(max_length=7, unique=True)
    modelo = models.CharField(max_length=50)
    cor = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.modelo} ({self.placa})"

class Visitante(models.Model):
    # Verifique se estes dois campos estão exatamente assim:
    nome = models.CharField(max_length=100)
    data_visita = models.DateField()
    
    # O restante do seu código do QR Code
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.qr_code:
            # Note que aqui você usa self.nome, então o campo 'nome' PRECISA existir acima
            qr_image = qrcode.make(f"Visitante: {self.nome} | ID: {self.id}")
            canvas = BytesIO()
            qr_image.save(canvas, format='PNG')
            fname = f'qr-{self.nome}.png'
            self.qr_code.save(fname, File(canvas), save=False)
        super().save(*args, **kwargs)
        
class ReservaPiscina(models.Model):
    morador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data = models.DateField()
    # Vamos trabalhar com faixas horárias fixas (ex: 09:00, 10:00, 11:00)
    hora_inicio = models.TimeField()

    def clean(self):
        # 1. Verificar se já existem 2 casas diferentes agendadas para o mesmo dia e hora
        conflitos = ReservaPiscina.objects.filter(
            data=self.data, 
            hora_inicio=self.hora_inicio
        ).count()

        if conflitos >= 2:
            raise ValidationError(
                f"Lamento! O horário das {self.hora_inicio} já atingiu o limite de 2 casas."
            )

        # 2. Evitar que o mesmo morador reserve dois horários seguidos (opcional, mas justo)
        ja_reservou_hoje = ReservaPiscina.objects.filter(
            morador=self.morador, 
            data=self.data
        ).exists()
        
        if ja_reservou_hoje and not self.pk: # Se for uma nova reserva
            raise ValidationError("Cada casa pode realizar apenas 1 reserva de piscina por dia.")

    def __str__(self):
        return f"Piscina: {self.morador.casa_bloco} em {self.data} às {self.hora_inicio}"
    

class Aviso(models.Model):
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    data_postagem = models.DateTimeField(auto_now_add=True)
    importante = models.BooleanField(default=False) # Para destacar em dourado

    def __str__(self):
        return self.titulo

class Ocorrencia(models.Model):
    STATUS_CHOICES = [
        ('ABERTO', 'Aberto') ,
        ('RECEBIDO', 'Recebido pela Portaria'),
        ('RESOLVIDO', 'Resolvido'),
    ]
    morador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    data_registro = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='ABERTO')
    resposta_gestao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.titulo} - {self.morador.casa_bloco}"
    
class Encomenda(models.Model):
    # CAMPOS ORIGINAIS (Que o formulário está procurando)
    morador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='encomendas')
    descricao = models.CharField(max_length=255, verbose_name="Descrição do Pacote")
    data_recebimento = models.DateTimeField(default=timezone.now)

    # NOVOS CAMPOS PARA CONTROLE DE ENTREGA
    entregue = models.BooleanField(default=False)
    data_entrega = models.DateTimeField(null=True, blank=True)
    retirado_por = models.CharField(max_length=100, null=True, blank=True, help_text="Nome de quem buscou")
    porteiro_entrega = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='entregas_realizadas'
    )

    def __str__(self):
        # Usamos getattr para evitar erro caso o morador ainda não tenha sido carregado
        nome_morador = self.morador.get_full_name() if self.morador else "Sem Morador"
        status = 'Entregue' if self.entregue else 'Pendente'
        return f"Pacote: {nome_morador} - {status}"
    
class Balancete(models.Model):
    titulo = models.CharField(max_length=100)
    mes_referencia = models.DateField()
    arquivo = models.FileField(upload_to='balancetes/') # <-- Este é o campo do PDF
    data_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo