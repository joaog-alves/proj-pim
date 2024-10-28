from django.contrib.auth.models import Group, User
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Especialidade, Uf

@receiver(post_migrate)
def setup_default_data(sender, **kwargs):
    # Verifica se o app é 'benessere'
    if sender.name == 'benessere':
        # Criar grupos padrão
        group_names = ["Medico", "Gestor", "Recepcionista"]
        for group_name in group_names:
            Group.objects.get_or_create(name=group_name)

        # Criar especialidades padrão
        default_specialties = [
            'Geral', 'Cardiologia', 'Dermatologia', 'Ginecologia',
            'Pediatria', 'Neurologia', 'Ortopedia', 'Oftalmologia',
            'Psiquiatria', 'Endocrinologia', 'Urologia'
        ]
        for specialty in default_specialties:
            Especialidade.objects.get_or_create(nome=specialty)

        # Criar UFs padrão
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
        for uf_data in initial_ufs:
            Uf.objects.get_or_create(sigla=uf_data['sigla'], nome=uf_data['nome'])

        # Criar o usuário gestor inicial
        if not User.objects.filter(username='gestor_inicial').exists():
            gestor_inicial = User.objects.create_user(
                username='gestor_inicial',
                email='gestor@example.com',
                password='senha_segura123'
            )
            # Adiciona o usuário ao grupo "Gestor"
            gestor_group, _ = Group.objects.get_or_create(name='Gestor')
            gestor_inicial.groups.add(gestor_group)
            gestor_inicial.is_staff = True  # Permissão de staff para acessar o admin
            gestor_inicial.save()
            print('Usuário gestor inicial criado: gestor_inicial (senha: senha_segura123)')
