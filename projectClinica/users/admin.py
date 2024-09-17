from atexit import register
from django.contrib import admin
from .models import *

# Register your models here.
from django.contrib import admin
from .models import Usuario

class UsuarioAdmin(admin.ModelAdmin):
    # Campos que você deseja exibir na lista de usuários
    list_display = ('username', 'nome', 'cpf', 'email', 'tipo_usuario', 'is_active')

    # Campos que você deseja adicionar ao filtro lateral
    list_filter = ('tipo_usuario', 'is_active')

    # Adiciona campos para edição na forma de grupos
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações pessoais', {'fields': ('nome', 'cpf', 'endereco', 'telefone', 'email', 'data_nascimento', 'data_admissao', 'tipo_usuario')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas importantes', {'fields': ('last_login', 'date_joined')}),
    )

    # Campos que serão exibidos apenas como leitura (não editáveis)
    readonly_fields = ('last_login', 'date_joined')

    # Adiciona filtros e campos de pesquisa
    search_fields = ('username', 'nome', 'cpf', 'email')

class AtendenteAdmin(admin.ModelAdmin):
    list_display = ('usuario',)
    search_fields = ('usuario__username', 'usuario__nome')

class MedicoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'especialidade', 'crm')
    search_fields = ('usuario__username', 'usuario__nome', 'crm')

class GerenteAdmin(admin.ModelAdmin):
    list_display = ('usuario',)
    search_fields = ('usuario__username', 'usuario__nome')

admin.site.register(Uf)
admin.site.register(Cidade)
admin.site.register(UnidadeClinica)
admin.site.register(Especialidade)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Atendente, AtendenteAdmin)
admin.site.register(Medico, MedicoAdmin)
admin.site.register(Gerente, GerenteAdmin)
admin.site.register(Paciente)
admin.site.register(Consulta)
admin.site.register(Pagamento)