from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group
from django.apps import AppConfig

# Cria os grupos necessários após a migração
def create_default_groups(sender, **kwargs):
    groups = ['Medico', 'Gerente', 'Recepcionista']
    for group_name in groups:
        Group.objects.get_or_create(name=group_name)

class BenessereConfig(AppConfig):
    name = 'benessere'

    def ready(self):
        # Conecta o sinal post_migrate para criar grupos
        post_migrate.connect(create_default_groups, sender=self)
