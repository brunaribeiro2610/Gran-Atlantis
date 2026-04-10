from django.utils import timezone
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
import urllib
from .forms import AvisoForm, CadastroFuncionarioForm, EncomendaForm, ReservaPiscinaForm, VeiculoForm, VisitanteForm, CadastroMoradorForm, BalanceteForm
from .models import Aviso, Encomenda, Ocorrencia, ReservaSalao, Veiculo, Visitante, ReservaPiscina, Balancete
from django.contrib import messages
import qrcode
from django.conf import settings
import os
from datetime import date
import urllib.parse

# --- DASHBOARD PRINCIPAL ---
@login_required
def dashboard(request):
    # 1. Padroniza e limpa espaços
    role_db = str(request.user.role).strip().upper() if request.user.role else "MORADOR"
    
    avisos = Aviso.objects.all().order_by('-data_postagem')
    balancetes = Balancete.objects.all().order_by('-mes_referencia')[:12]
    
    # --- O AJUSTE ESTÁ AQUI: ADICIONAMOS O SELECT_RELATED ---
    encomendas_gerais = Encomenda.objects.filter(entregue=False).select_related('morador').order_by('-data_recebimento')
    reservas_p_hoje = ReservaPiscina.objects.filter(data=date.today()).select_related('morador')
    reservas_s_hoje = ReservaSalao.objects.filter(data=date.today()).select_related('morador')

    context = {
        'user_role_fixed': role_db,
        'avisos': avisos,
        'balancetes': balancetes,
        'today': date.today(),
    }

    # SE FOR EQUIPE (PORTEIRO, SINDICO, OU STAFF)
    if role_db in ["PORTEIRO", "SINDICO", "SÍNDICO", "PORTARIA"] or request.user.is_staff:
        context['encomendas'] = encomendas_gerais
        context['visitas'] = Visitante.objects.all().order_by('-data_visita')[:10]
        context['reservas_piscina_hoje'] = reservas_p_hoje
        context['reservas_salao_hoje'] = reservas_s_hoje
        context['ocorrencias'] = Ocorrencia.objects.all().order_by('-data_registro')
    
    # SE FOR MORADOR
    else:
        context['encomendas'] = Encomenda.objects.filter(morador=request.user, entregue=False)
        context['visitas'] = Visitante.objects.all().order_by('-data_visita')[:5]
        context['minhas_reservas_piscina'] = ReservaPiscina.objects.filter(morador=request.user, data__gte=date.today())
        context['minhas_reservas_salao'] = ReservaSalao.objects.filter(morador=request.user, data__gte=date.today())
        context['ocorrencias'] = Ocorrencia.objects.filter(morador=request.user).order_by('-data_registro')

    return render(request, 'core/dashboard.html', context)

# --- OCORRÊNCIAS ---
@login_required
def criar_ocorrencia(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        if titulo and descricao:
            Ocorrencia.objects.create(
                morador=request.user,
                titulo=titulo,
                descricao=descricao,
                status='ABERTO'
            )
            messages.success(request, "Ocorrência registrada com sucesso!")
            return redirect('core:dashboard')
    return render(request, 'core/registrar_ocorrencia.html')


@login_required
def minhas_ocorrencias(request):
    user_role = str(request.user.role).upper()
    if user_role == "MORADOR":
        ocorrencias = Ocorrencia.objects.filter(morador=request.user).order_by('-data_registro')
    else:
        ocorrencias = Ocorrencia.objects.all().order_by('-data_registro')
    
    return render(request, 'core/minhas_ocorrencias.html', {
        'ocorrencias': ocorrencias,
        'user_role_fixed': user_role
    })

@login_required
def marcar_recebido(request, pk):
    ocorrencia = get_object_or_404(Ocorrencia, pk=pk)
    ocorrencia.status = 'RECEBIDO'
    ocorrencia.save()
    messages.success(request, "Status atualizado!")
    return redirect('core:minhas_ocorrencias')

# --- VEÍCULOS ---
@login_required
def cadastrar_veiculo(request):
    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            veiculo = form.save(commit=False)
            veiculo.morador = request.user
            veiculo.save()
            messages.success(request, "Veículo cadastrado!")
            return redirect('core:dashboard')
    else:
        form = VeiculoForm()
    
    meus_veiculos = Veiculo.objects.filter(morador=request.user)
    return render(request, 'core/veiculos.html', {'form': form, 'veiculos': meus_veiculos})

@login_required
def excluir_veiculo(request, pk):
    veiculo = get_object_or_404(Veiculo, pk=pk, morador=request.user)
    veiculo.delete()
    messages.success(request, "Veículo removido.")
    return redirect('core:cadastrar_veiculo')

# --- PISCINA E SALÃO ---
@login_required
def agendar_piscina(request):
    horarios = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"]
    
    if request.method == 'POST':
        try:
            data_vinda_do_html = request.POST.get('data')
            hora_vinda_do_html = request.POST.get('hora')

            nova_reserva = ReservaPiscina(
                morador=request.user,
                data=data_vinda_do_html,
                hora_inicio=hora_vinda_do_html
            )
            
            nova_reserva.full_clean() # Roda as validações do models.py
            nova_reserva.save()
            
            # Em vez de redirect imediato, vamos renderizar o sucesso
            # para o morador ver que a reserva na unidade dele (Rua/Casa) foi feita
            return render(request, 'core/agendar_piscina.html', {
                'horarios': horarios,
                'reserva_sucesso': nova_reserva,
                'sucesso': True
            })
            
        except ValidationError as e:
            # Pega a mensagem de erro que você escreveu no models.py
            msg = e.message_dict.get('__all__', e.messages)[0] if hasattr(e, 'message_dict') else str(e)
            messages.error(request, msg)
        except Exception as e:
            messages.error(request, f"Erro inesperado: {e}")
            
    return render(request, 'core/agendar_piscina.html', {
        'horarios': horarios,
        'today': date.today().strftime('%Y-%m-%d')
    })
@login_required
def cancelar_piscina(request, pk):
    reserva = get_object_or_404(ReservaPiscina, pk=pk, morador=request.user)
    reserva.delete()
    return redirect('core:dashboard')

@login_required
def agendar_salao(request):
    if request.method == 'POST':
        try:
            reserva = ReservaSalao(morador=request.user, data=request.POST.get('data'))
            reserva.full_clean()
            reserva.save()
            return redirect('core:dashboard')
        except ValidationError:
            messages.error(request, "Data indisponível.")
    return render(request, 'core/agendar_salao.html')

@login_required
def cancelar_salao(request, pk):
    reserva = get_object_or_404(ReservaSalao, pk=pk, morador=request.user)
    reserva.delete()
    return redirect('core:dashboard')

def SeuFormVisita(*args, **kwargs):
    raise NotImplementedError

# --- VISITAS E QR CODE ---

@login_required
def agendar_visita(request):
    if request.method == 'POST':
        form = VisitanteForm(request.POST) 
        if form.is_valid():
            visita = form.save(commit=False)
            # Se o seu model tiver um campo 'morador', salvamos quem está logado
            # visita.morador = request.user 
            visita.save()

            return render(request, 'core/agendar_visita.html', {
                'form': VisitanteForm(), 
                'visita': visita,
                'sucesso': True,
                # Passamos a unidade do morador logado para o HTML
                'unidade': "Rua E 4" # Ou request.user.perfil.unidade (depende do seu model)
            })

def detalhes_visita(request, visita_id):
    from django.shortcuts import get_object_or_404
    # Busca o visitante no banco de dados
    visita = get_object_or_404(Visitante, id=visita_id)
    return render(request, 'core/detalhes_visita.html', {'visita': visita})

@login_required
def lista_visitas(request):
    # Mantendo a lógica simplificada para evitar o erro de campo 'morador' que você teve
    visitas = Visitante.objects.all().order_by('-data_visita')
    return render(request, 'core/lista_visitas.html', {'visitas': visitas})

@login_required
def excluir_visitante(request, visitante_id):
    visitante = get_object_or_404(Visitante, id=visitante_id)
    visitante.delete()
    messages.success(request, "Convite removido.")
    return redirect('core:lista_visitas')

@login_required
def autorizar_visita(request, visita_id):
    visita = get_object_or_404(Visitante, id=visita_id)
    if request.method == "POST":
        visita.horario_entrada = timezone.now()
        visita.save()
        messages.success(request, "Entrada autorizada!")
        return redirect('core:lista_visitas')
    return render(request, 'core/confirmar_entrada.html', {'visita': visita})

# --- GESTÃO (SÍNDICO E PORTEIRO) ---
@login_required
def criar_aviso(request):
    if str(request.user.role).upper() != 'SINDICO': return redirect('core:dashboard')
    if request.method == 'POST':
        form = AvisoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:dashboard')
    return render(request, 'core/criar_aviso.html', {'form': AvisoForm()})

@login_required
def excluir_aviso(request, pk):
    if str(request.user.role).upper() == 'SINDICO':
        get_object_or_404(Aviso, pk=pk).delete()
    return redirect('core:dashboard')

@login_required
def cadastrar_funcionario(request):
    if str(request.user.role).upper() != 'SINDICO': return redirect('core:dashboard')
    if request.method == 'POST':
        form = CadastroFuncionarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.role = 'PORTEIRO'
            user.is_staff = True
            user.save()
            messages.success(request, "Porteiro cadastrado com sucesso!")
            return redirect('core:dashboard')
    return render(request, 'core/cadastrar_porteiro.html', {'form': CadastroFuncionarioForm()})

@login_required
def registrar_encomenda(request):
    if request.method == 'POST':
        form = EncomendaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Encomenda registrada!")
            return redirect('core:dashboard')
    return render(request, 'core/registrar_encomenda.html', {'form': EncomendaForm()})

@login_required
def entregar_encomenda(request, pk):
    encomenda = get_object_or_404(Encomenda, pk=pk)
    if request.method == 'POST':
        # Captura quem retirou e registra o porteiro logado
        quem_retirou = request.POST.get('retirado_por')
        if quem_retirou:
            encomenda.entregue = True
            encomenda.data_entrega = timezone.now()
            encomenda.retirado_por = quem_retirou.upper()
            encomenda.porteiro_entrega = request.user
            encomenda.save()
            messages.success(request, "Encomenda entregue com sucesso!")
        else:
            messages.error(request, "Por favor, informe quem retirou.")
        return redirect('core:dashboard')
    return render(request, 'core/entregar_encomenda.html', {'encomenda': encomenda})

@login_required
def upload_balancete(request):
    if request.method == 'POST':
        form = BalanceteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('core:dashboard')
    return render(request, 'core/upload_balancete.html', {'form': BalanceteForm()})

@login_required
def enviar_balancete(request):
    if request.method == 'POST':
        mes = request.POST.get('mes_referencia')
        arquivo = request.FILES.get('arquivo')
        if mes and arquivo:
            Balancete.objects.create(
                mes_referencia=f"{mes}-01",
                arquivo=arquivo
            )
            messages.success(request, "Balancete enviado!")
            return redirect('core:dashboard')
    return render(request, 'core/enviar_balancete.html')

@login_required
def excluir_balancete(request, id):
    if str(request.user.role).upper() == 'SINDICO':
        get_object_or_404(Balancete, id=id).delete()
        messages.success(request, "Balancete removido.")
    return redirect('core:dashboard')

# --- CADASTRO E PORTARIA ---
def cadastro_morador(request):
    if request.method == 'POST':
        form = CadastroMoradorForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'MORADOR'
            user.is_active = False # Aguarda aprovação
            user.save()
            messages.success(request, "Cadastro realizado! Aguarde a aprovação do síndico.")
            return redirect('login')
    else:
        form = CadastroMoradorForm()
    return render(request, 'core/cadastro.html', {'form': form})

@login_required
def portaria_scanner(request):
    user_role = str(request.user.role).upper()
    if user_role not in ["PORTEIRO", "SINDICO", "SÍNDICO"]:
        messages.error(request, "Acesso restrito.")
        return redirect('core:dashboard')
    return render(request, 'core/portaria_scanner.html')

@login_required
def mapa_piscina_portaria(request):
    # O segredo é o 'agendamentos' e o 'select_related'
    agendamentos = ReservaPiscina.objects.filter(
        data=date.today()
    ).select_related('morador') # Isso aqui "puxa" a casa_bloco para o porteiro
    
    return render(request, 'core/mapa_piscina.html', {
        'agendamentos': agendamentos, 
        'hoje': date.today()
    })

@login_required
def relatorio_financeiro(request):
    if str(request.user.role).upper() != 'SINDICO':
        return redirect('core:dashboard')
    return render(request, 'core/relatorio_financeiro.html')