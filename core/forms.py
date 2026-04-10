
from django import forms
from .models import Encomenda, Veiculo, Visitante, Usuario, Aviso, Balancete, ReservaPiscina
from django.contrib.auth.forms import UserCreationForm
from django.core.files import File




class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        # Adicione 'tipo' na lista de campos
        fields = ['tipo', 'placa', 'modelo', 'cor'] 
        widgets = {
            # Novo widget para o Tipo (Carro ou Moto)
            'tipo': forms.Select(attrs={'class': 'form-control form-control-atlantis'}),
            
            'placa': forms.TextInput(attrs={'class': 'form-control form-control-atlantis', 'placeholder': 'ABC1D23'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control form-control-atlantis', 'placeholder': 'Ex: Corolla'}),
            'cor': forms.TextInput(attrs={'class': 'form-control form-control-atlantis', 'placeholder': 'Ex: Prata'}),
        }
        
        
class VisitanteForm(forms.ModelForm):
    class Meta:
        model = Visitante
        # Use EXATAMENTE os nomes que estão no models.py
        fields = ['nome', 'data_visita'] 
        widgets = {
            'data_visita': forms.DateInput(attrs={'type': 'date'}),
        }
        

class CadastroMoradorForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ("username", "email", "casa_bloco", "telefone")
        

class CadastroFuncionarioForm(UserCreationForm):
    nome_completo = forms.CharField(max_length=150, label="Nome Completo")
    cpf = forms.CharField(max_length=14, label="CPF")

    class Meta(UserCreationForm.Meta):
        model = Usuario
        # Aqui listamos apenas o que o porteiro precisa ter
        fields = ("username", "nome_completo", "email", "cpf", "telefone")
        

class EncomendaForm(forms.ModelForm):
    class Meta:
        model = Encomenda
        # Verifique se esses nomes existem exatamente assim no seu models.py
        fields = ['morador', 'descricao'] 
        widgets = {
            'morador': forms.Select(attrs={'class': 'form-control form-control-atlantis'}),
            'descricao': forms.TextInput(attrs={
                'class': 'form-control form-control-atlantis', 
                'placeholder': 'Ex: Pacote Amazon, Caixa Grande...'
            }),
        }        
        
class AvisoForm(forms.ModelForm):
    class Meta:
        model = Aviso
        fields = ['titulo', 'conteudo', 'importante']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control bg-dark text-gold border-secondary'}),
            'conteudo': forms.Textarea(attrs={'class': 'form-control bg-dark text-gold border-secondary', 'rows': 4}),
            'importante': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        


class BalanceteForm(forms.ModelForm):
    class Meta:
        model = Balancete
        fields = ['titulo', 'mes_referencia', 'arquivo'] # 'arquivo' tem que estar aqui!
        widgets = {
            'arquivo': forms.FileInput(attrs={'class': 'form-control bg-dark text-white'}),
        }
        
class ReservaPiscinaForm(forms.ModelForm):
    # Criamos a lista de horários para o usuário escolher
    HORARIOS = [
        ('08:00', '08:00 às 09:00'),
        ('09:00', '09:00 às 10:00'),
        ('10:00', '10:00 às 11:00'),
        ('11:00', '11:00 às 12:00'),
        ('12:00', '12:00 às 13:00'),
        ('13:00', '13:00 às 14:00'),
        ('14:00', '14:00 às 15:00'),
        ('15:00', '15:00 às 16:00'),
        ('16:00', '16:00 às 17:00'),
        ('17:00', '17:00 às 18:00'),
        ('18:00', '18:00 às 19:00'),
    ]

    hora_inicio = forms.ChoiceField(
        choices=HORARIOS, 
        widget=forms.Select(attrs={'class': 'form-select form-control-atlantis'})
    )

    class Meta:
        model = ReservaPiscina
        fields = ['data', 'hora_inicio']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-atlantis'}),
        }