# benessere/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .forms import *
from .models import *

# Personalização da exibição de usuário no admin
class CustomUserAdmin(BaseUserAdmin):
    add_form = UserCreationForm

    # Configura o que será exibido no formulário de criação de usuário
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'groups'),  # Exibe o campo de grupos após as senhas
        }),
    )

    # Configuração para editar os usuários
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

# Registre o UserAdmin personalizado
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Registro dos modelos do benessere
@admin.register(Uf)
class UfAdmin(admin.ModelAdmin):
    list_display = ('sigla', 'nome')
    search_fields = ('sigla', 'nome')

@admin.register(Cidade)
class CidadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'uf')
    search_fields = ('nome',)
    list_filter = ('uf',)

@admin.register(UnidadeClinica)
class UnidadeClinicaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cidade', 'telefone')
    search_fields = ('nome', 'cidade__nome')
    list_filter = ('cidade',)

@admin.register(Especialidade)
class EspecialidadeAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'especialidade', 'crm')
    search_fields = ('usuario__username', 'crm')
    list_filter = ('especialidade',)

@admin.register(Recepcionista)
class RecepcionistaAdmin(admin.ModelAdmin):
    list_display = ('usuario',)
    search_fields = ('usuario__username',)

@admin.register(Gestor)
class GestorAdmin(admin.ModelAdmin):
    list_display = ('usuario',)
    search_fields = ('usuario__username',)

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'telefone', 'email')
    search_fields = ('nome', 'cpf', 'email')

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'medico', 'data_hora', 'unidade_clinica')
    search_fields = ('paciente__nome', 'medico__usuario__username')
    list_filter = ('data_hora', 'unidade_clinica')

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'consulta', 'valor', 'data_pagamento')
    search_fields = ('paciente__nome', 'consulta__medico__usuario__username')
    list_filter = ('data_pagamento',)

@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    list_display = ('consulta', 'data', 'hora')
    search_fields = ('consulta__paciente__nome',)
    list_filter = ('data',)
