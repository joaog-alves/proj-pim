# benessere/forms.py
from django import forms
from .models import *

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['paciente', 'medico', 'data_hora', 'unidade_clinica', 'observacoes']
        widgets = {
            'data_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        labels = {
            'paciente': 'Paciente',
            'medico': 'Médico',
            'data_hora': 'Data e Hora',
            'unidade_clinica': 'Unidade Clínica',
            'observacoes': 'Observações',
        }

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'cpf', 'telefone', 'email', 'data_nascimento', 'endereco']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'nome': 'Nome do Paciente',
            'cpf': 'CPF',
            'telefone': 'Telefone',
            'email': 'Email',
            'data_nascimento': 'Data de Nascimento',
            'endereco': 'Endereço',
        }

class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['paciente', 'consulta', 'valor', 'data_pagamento']
        widgets = {
            'data_pagamento': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }