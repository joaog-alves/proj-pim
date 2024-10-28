# benessere/signals.py
from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import *
from django.db import migrations

@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    group_names = ["Medico", "Gestor", "Recepcionista"]
    for group_name in group_names:
        Group.objects.get_or_create(name=group_name)

@receiver(post_migrate)
def add_default_specialties(sender, **kwargs):
    if sender.name == 'benessere':
        default_specialties = [
            'Geral',
            'Cardiologia',
            'Dermatologia',
            'Ginecologia',
            'Pediatria',
            'Neurologia',
            'Ortopedia',
            'Oftalmologia',
            'Psiquiatria',
            'Endocrinologia',
            'Urologia'

        ]
        for specialty in default_specialties:
            Especialidade.objects.get_or_create(nome=specialty)

@receiver(post_migrate)
def create_default_ufs(sender, **kwargs):
    # Lista de UFs para adicionar
    initial_ufs = [
        {'sigla': 'AC', 'nome': 'Acre'},
        {'sigla': 'AL', 'nome': 'Alagoas'},
        {'sigla': 'AP', 'nome': 'Amapá'},
        {'sigla': 'AM', 'nome': 'Amazonas'},
        {'sigla': 'BA', 'nome': 'Bahia'},
        {'sigla': 'CE', 'nome': 'Ceará'},
        {'sigla': 'DF', 'nome': 'Distrito Federal'},
        {'sigla': 'ES', 'nome': 'Espírito Santo'},
        {'sigla': 'GO', 'nome': 'Goiás'},
        {'sigla': 'MA', 'nome': 'Maranhão'},
        {'sigla': 'MT', 'nome': 'Mato Grosso'},
        {'sigla': 'MS', 'nome': 'Mato Grosso do Sul'},
        {'sigla': 'MG', 'nome': 'Minas Gerais'},
        {'sigla': 'PA', 'nome': 'Pará'},
        {'sigla': 'PB', 'nome': 'Paraíba'},
        {'sigla': 'PR', 'nome': 'Paraná'},
        {'sigla': 'PE', 'nome': 'Pernambuco'},
        {'sigla': 'PI', 'nome': 'Piauí'},
        {'sigla': 'RJ', 'nome': 'Rio de Janeiro'},
        {'sigla': 'RN', 'nome': 'Rio Grande do Norte'},
        {'sigla': 'RS', 'nome': 'Rio Grande do Sul'},
        {'sigla': 'RO', 'nome': 'Rondônia'},
        {'sigla': 'RR', 'nome': 'Roraima'},
        {'sigla': 'SC', 'nome': 'Santa Catarina'},
        {'sigla': 'SP', 'nome': 'São Paulo'},
        {'sigla': 'SE', 'nome': 'Sergipe'},
        {'sigla': 'TO', 'nome': 'Tocantins'},
    ]

    # Cria as UFs, se ainda não existirem
    for uf_data in initial_ufs:
        Uf.objects.get_or_create(sigla=uf_data['sigla'], nome=uf_data['nome'])

class Migration(migrations.Migration):

    dependencies = [
        ('benessere', 'previous_migration_file'),
    ]

    operations = [
        migrations.RunPython(add_default_specialties),
    ]
