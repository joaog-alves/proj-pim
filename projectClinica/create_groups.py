# create_groups.py
from django.contrib.auth.models import Group

# Grupos que precisam ser criados
group_names = ["Medico", "Gerente", "Recepcionista"]

# Cria os grupos caso não existam
for group_name in group_names:
    Group.objects.get_or_create(name=group_name)
    
print("Grupos criados ou já existentes:", group_names)
