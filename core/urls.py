from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('ocorrencias/nova/', views.criar_ocorrencia, name='criar_ocorrencia'),
    path('ocorrencias/', views.minhas_ocorrencias, name='minhas_ocorrencias'),
    path('ocorrencias/recebido/<int:pk>/', views.marcar_recebido, name='marcar_recebido'),
    path('veiculos/cadastrar/', views.cadastrar_veiculo, name='cadastrar_veiculo'),
    path('veiculos/excluir/<int:pk>/', views.excluir_veiculo, name='excluir_veiculo'),
    path('piscina/agendar/', views.agendar_piscina, name='agendar_piscina'),
    path('piscina/cancelar/<int:pk>/', views.cancelar_piscina, name='cancelar_piscina'),
    path('salao/agendar/', views.agendar_salao, name='agendar_salao'),
    path('salao/cancelar/<int:pk>/', views.cancelar_salao, name='cancelar_salao'),
    path('visitas/agendar/', views.agendar_visita, name='agendar_visita'),
    path('visitas/', views.lista_visitas, name='lista_visitas'),
    path('visita/excluir/<int:visitante_id>/', views.excluir_visitante, name='excluir_visitante'),
    path('visita/detalhes/<int:visita_id>/', views.detalhes_visita, name='detalhes_visita'),
    path('portaria/autorizar/<int:visita_id>/', views.autorizar_visita, name='autorizar_visita'),
    path('avisos/criar/', views.criar_aviso, name='criar_aviso'),
    path('avisos/excluir/<int:pk>/', views.excluir_aviso, name='excluir_aviso'),
    path('funcionarios/cadastrar/', views.cadastrar_funcionario, name='cadastrar_funcionario'),
    path('encomendas/registrar/', views.registrar_encomenda, name='registrar_encomenda'),
    path('encomenda/entregar/<int:pk>/', views.entregar_encomenda, name='entregar_encomenda'),
    path('balancetes/upload/', views.upload_balancete, name='upload_balancete'),
    path('balancetes/excluir/<int:id>/', views.excluir_balancete, name='excluir_balancete'),
    path('balancetes/enviar/', views.enviar_balancete, name='enviar_balancete'),
    path('cadastro/', views.cadastro_morador, name='cadastro_morador'),
    
    
    
]