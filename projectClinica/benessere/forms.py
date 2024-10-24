# benessere/forms.py
from django import forms
from .models import *
from django.contrib.auth.models import User, Group

class CustomUserCreationForm(forms.ModelForm):
    USER_TYPE_CHOICES = [
        ('Medico', 'Médico'),
        ('Gerente', 'Gerente'),
        ('Recepcionista', 'Recepcionista'),
    ]

    tipo_usuario = forms.ChoiceField(choices=USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'tipo_usuario']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        
        if commit:
            user.save()
            # Adiciona o usuário ao grupo baseado no tipo selecionado
            group_name = self.cleaned_data['tipo_usuario']
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
        
        return user

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
