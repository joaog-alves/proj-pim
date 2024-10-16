# benessere/admin.py
from django.contrib import admin
from .models import Uf, Cidade, UnidadeClinica, Especialidade, Medico, Atendente, Gerente, Paciente, Consulta, Pagamento, CheckIn

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

@admin.register(Atendente)
class AtendenteAdmin(admin.ModelAdmin):
    list_display = ('usuario',)
    search_fields = ('usuario__username',)

@admin.register(Gerente)
class GerenteAdmin(admin.ModelAdmin):
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
