from django.contrib import admin
from .models import Usuario, Veiculo, Visitante, ReservaPiscina, Aviso, Ocorrencia

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'casa_bloco', 'role', 'telefone', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'casa_bloco')
    # Permite ao síndico ativar moradores com um clique
    actions = ['ativar_moradores']

    def ativar_moradores(self, request, queryset):
        queryset.update(is_active=True)
    ativar_moradores.short_description = "Aprovar acesso dos moradores selecionados"

@admin.register(Aviso)
class AvisoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_postagem', 'importante')
    list_editable = ('importante',) # Muda o status de importante direto na lista

@admin.register(ReservaPiscina)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('morador', 'data', 'hora_inicio')
    list_filter = ('data', 'hora_inicio')

@admin.register(Ocorrencia)
class OcorrenciaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'morador', 'status', 'data_registro')
    list_filter = ('status',)
    # O síndico clica na ocorrência e preenche a 'resposta_gestao'
    fields = ('morador', 'titulo', 'descricao', 'status', 'resposta_gestao')
    readonly_fields = ('morador', 'titulo', 'descricao')

# Registros simples para consulta
admin.site.register(Veiculo)
admin.site.register(Visitante)
admin.site.site_header = "Gran Atlantis - Gestão Administrativa"
admin.site.site_title = "Painel Síndico"
admin.site.index_title = "Bem-vindo à Administração do Gran Atlantis"