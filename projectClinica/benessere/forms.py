# benessere/forms.py
from django import forms
from .models import *
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.filter(name__in=["Medico", "Gestor", "Recepcionista"]),
        required=True,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'groups-checkbox'}),
        label='Grupos'
    )

    # Campos adicionais para médicos
    especialidade = forms.ModelChoiceField(
        queryset=Especialidade.objects.all(),
        required=False,
        label='Especialidade',
        widget=forms.Select(attrs={'class': 'medico-field'})
    )
    crm = forms.CharField(
        max_length=20,
        required=False,
        label='CRM',
        widget=forms.TextInput(attrs={'class': 'medico-field'})
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'groups', 'especialidade', 'crm']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        # Verifica se a foto foi fornecida antes de criar o perfil do usuário
        if self.cleaned_data.get('photo'):
            UserProfile.objects.create(user=user, photo=self.cleaned_data['photo'])
        else:
            # Cria o perfil sem a foto, se necessário
            UserProfile.objects.get_or_create(user=user)
        return user


    def clean(self):
        cleaned_data = super().clean()
        groups = cleaned_data.get('groups')
        especialidade = cleaned_data.get('especialidade')
        crm = cleaned_data.get('crm')

        # Verificar se o grupo Médico foi selecionado e se os campos necessários estão preenchidos
        if any(group.name == "Medico" for group in groups):
            if not especialidade or not crm:
                raise forms.ValidationError("Para médicos, é necessário informar a especialidade e o CRM.")
        
        return cleaned_data


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

class UnidadeClinicaForm(forms.ModelForm):
    # Campo para digitar o nome da cidade manualmente
    cidade = forms.CharField(
        max_length=40,
        required=True,
        label='Cidade',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='Digite o nome da cidade'
    )

    # Campo para selecionar a UF
    uf = forms.ModelChoiceField(
        queryset=Uf.objects.all(),
        required=True,
        label='UF',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = UnidadeClinica
        fields = ['nome', 'endereco', 'telefone']
        labels = {
            'nome': 'Nome da Unidade',
            'endereco': 'Endereço',
            'telefone': 'Telefone',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        unidade_clinica = super().save(commit=False)

        # Recupera a UF selecionada e o nome da cidade digitado
        uf = self.cleaned_data.get('uf')
        cidade_nome = self.cleaned_data.get('cidade')

        if cidade_nome and uf:
            # Cria a nova cidade e a associa à unidade
            cidade, created = Cidade.objects.get_or_create(nome=cidade_nome, uf=uf)
            unidade_clinica.cidade = cidade

        if commit:
            unidade_clinica.save()
        return unidade_clinica

class DiagnosticoForm(forms.ModelForm):
    class Meta:
        model = Diagnostico
        fields = ['descricao']

class MedicacaoForm(forms.ModelForm):
    class Meta:
        model = Medicacao
        fields = ['nome', 'dosagem', 'instrucoes']
