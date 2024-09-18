from atexit import register
from django.contrib import admin
from .models import *
from django import forms

class UsuarioAdminForm(forms.ModelForm):
    especialidade = forms.ModelChoiceField(queryset=Especialidade.objects.all(), required=False)

    class Meta:
        model = Usuario
        fields = '__all__'

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()

        # Criar perfil de médico se o tipo for "medico"
        if user.tipo_usuario == 'medico' and not hasattr(user, 'medico'):
            especialidade = self.cleaned_data.get('especialidade')
            if especialidade:
                Medico.objects.create(usuario=user, especialidade=especialidade, crm="CRM")
        return user

class UsuarioAdmin(admin.ModelAdmin):
    form = UsuarioAdminForm
    list_display = ('username', 'nome', 'cpf', 'email', 'tipo_usuario', 'is_active')
    list_filter = ('tipo_usuario', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações pessoais', {'fields': ('nome', 'cpf', 'endereco', 'telefone', 'email', 'data_nascimento', 'data_admissao', 'tipo_usuario')}),  # Adiciona o campo especialidade
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('last_login', 'date_joined')
    search_fields = ('username', 'nome', 'cpf', 'email')

    def save_model(self, request, obj, form, change):
        # Primeiro salva o objeto Usuario
        super().save_model(request, obj, form, change)

        # Depois de salvar o usuario, cria o perfil relacionado, se ainda não existir
        if obj.tipo_usuario == 'medico' and not hasattr(obj, 'medico'):
            especialidade = form.cleaned_data.get('especialidade')
            if especialidade:
                Medico.objects.create(usuario=obj, especialidade=especialidade, crm="CRM")
        elif obj.tipo_usuario == 'atendente' and not hasattr(obj, 'atendente'):
            Atendente.objects.create(usuario=obj)
        elif obj.tipo_usuario == 'gerente' and not hasattr(obj, 'gerente'):
            Gerente.objects.create(usuario=obj)

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