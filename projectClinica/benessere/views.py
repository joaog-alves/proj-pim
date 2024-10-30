from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import group_required
from django.contrib.auth.models import User, Group
from .models import UserProfile



@login_required
def login_redirect(request):
    user = request.user
    
    # Verifica o grupo ao qual o usuário pertence e redireciona
    if user.groups.filter(name="Medico").exists():
        return redirect('med_consultas')
    elif user.groups.filter(name="Gestor").exists():
        return redirect('gestor_dashboard')
    elif user.groups.filter(name="Recepcionista").exists():
        return redirect('recp_consultas')
    else:
        return redirect('login')

@login_required
def acesso_negado(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redireciona para o login se o usuário não estiver autenticado
    return render(request, 'benessere/acesso_negado.html')

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
def upload_user_photo(request):
    if request.method == 'POST':
        # Verifica se o campo de foto foi enviado
        if 'photo' in request.FILES:
            photo = request.FILES['photo']
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            user_profile.photo = photo
            user_profile.save()
        else:
            # Cria ou obtém o perfil do usuário sem atualizar a foto
            UserProfile.objects.get_or_create(user=request.user)

        # Redirecionamento baseado no grupo do usuário
        if request.user.groups.filter(name='Gestor').exists():
            return redirect('gestor_dashboard')
        elif request.user.groups.filter(name='Medico').exists():
            return redirect('med_consultas')
        elif request.user.groups.filter(name='Recepcionista').exists():
            return redirect('recp_consultas')

    # Redirecionamento padrão caso o método não seja POST
    return redirect('gestor_dashboard')


@group_required("Recepcionista")
def recp_lista_consultas(request):
    consultas = Consulta.objects.all()
    return render(request, 'benessere/recp_consultas.html', {'consultas': consultas})

@group_required("Recepcionista")
def recp_adicionar_consulta(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('recp_consultas')
    else:
        form = ConsultaForm()

    return render(request, 'benessere/recp_adicionar_consulta.html', {'form': form})

@group_required("Recepcionista")
def recp_detalhes_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    checkin_exists = CheckIn.objects.filter(consulta=consulta).exists()
    
    return render(request, 'benessere/recp_detalhes_consulta.html', {
        'consulta': consulta,
        'checkin_exists': checkin_exists
    })

@group_required("Recepcionista")
def recp_editar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    if request.method == 'POST':
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            return redirect('recp_detalhes_consulta', consulta_id=consulta.id)
    else:
        form = ConsultaForm(instance=consulta)
    return render(request, 'benessere/recp_editar_consulta.html', {'form': form, 'consulta': consulta}) 

@group_required("Recepcionista")    
def remover_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    consulta.delete()
    messages.success(request, 'Consulta removida com sucesso.')
    return redirect('recp_consultas')

@group_required("Recepcionista")
def checkin_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    
    # Cria o registro de check-in, se não existir
    checkin, created = CheckIn.objects.get_or_create(consulta=consulta)
    
    if created:
        messages.success(request, 'Check-in realizado com sucesso!')
    else:
        messages.info(request, 'O check-in já foi realizado para esta consulta.')
    
    return redirect('recp_detalhes_consulta', consulta_id=consulta.id)

@group_required("Recepcionista")
def desfazer_checkin(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    checkin = CheckIn.objects.filter(consulta=consulta)
    
    if checkin.exists():
        checkin.delete()
        messages.success(request, 'Check-in desfeito com sucesso.')
    else:
        messages.info(request, 'Não há check-in para desfazer.')
    
    return redirect('recp_detalhes_consulta', consulta_id=consulta.id)

@group_required("Recepcionista")
def recp_lista_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'benessere/recp_pacientes.html', {'pacientes': pacientes})

def lista_mensagens(request):
    # Aqui você pode adicionar a lógica para buscar mensagens
    mensagens = []  # Exemplo: substitua pelo queryset real, se houver
    return render(request, 'benessere/recp_mensagens.html', {'mensagens': mensagens})

@group_required("Recepcionista")
def recp_detalhes_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    consultas = Consulta.objects.filter(paciente=paciente)  # Busca todas as consultas do paciente
    
    return render(request, 'benessere/recp_detalhes_paciente.html', {
        'paciente': paciente,
        'consultas': consultas
    })

@group_required("Recepcionista")
def recp_adicionar_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('recp_pacientes')
    else:
        form = PacienteForm()
    return render(request, 'benessere/recp_adicionar_paciente.html', {'form': form})

@group_required("Recepcionista")
def recp_editar_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('recp_detalhes_paciente', paciente_id=paciente.id)
    else:
        form = PacienteForm(instance=paciente)
    return render(request, 'benessere/recp_editar_paciente.html', {'form': form, 'paciente': paciente})

def lista_pagamentos(request):
    pagamentos = Pagamento.objects.all()
    return render(request, 'benessere/recp_pagamento.html', {'pagamentos': pagamentos})

def detalhes_pagamento(request, pagamento_id):
    pagamento = get_object_or_404(Pagamento, id=pagamento_id)
    return render(request, 'benessere/recp_visualizar_pagamento.html', {'pagamento': pagamento})

def adicionar_pagamento(request):
    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pagamento adicionado com sucesso.')
            return redirect('lista_pagamentos')
    else:
        form = PagamentoForm()
    return render(request, 'benessere/recp_adicionar_pagamento.html', {'form': form})

def editar_pagamento(request, pagamento_id):
    pagamento = get_object_or_404(Pagamento, id=pagamento_id)
    if request.method == 'POST':
        form = PagamentoForm(request.POST, instance=pagamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pagamento atualizado com sucesso.')
            return redirect('detalhes_pagamento', pagamento_id=pagamento.id)
    else:
        form = PagamentoForm(instance=pagamento)
    return render(request, 'benessere/recp_editar_pagamento.html', {'form': form, 'pagamento': pagamento})

@group_required('Medico')
def med_consultas(request):
    # Filtra as consultas apenas para o médico logado
    consultas = Consulta.objects.filter(medico__usuario=request.user)
    return render(request, 'benessere/med_consultas.html', {'consultas': consultas})

@group_required('Medico')
def med_mensagens(request):
    # Lógica para exibir as mensagens do médico
    return render(request, 'benessere/med_mensagens.html')

@group_required('Medico')
def med_detalhes_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    paciente = consulta.paciente

    return render(request, 'benessere/med_detalhes_consulta.html', {
        'consulta': consulta,
        'paciente': paciente
    })

def med_atendimento(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    paciente = consulta.paciente

    # Obtém ou cria o diagnóstico para a consulta específica
    diagnostico, created = Diagnostico.objects.get_or_create(consulta=consulta)

    if request.method == 'POST':
        diagnostico_form = DiagnosticoForm(request.POST, instance=diagnostico)
        medicacao_form = MedicacaoForm(request.POST)

        if diagnostico_form.is_valid():
            diagnostico = diagnostico_form.save()

            if medicacao_form.is_valid():
                medicacao = medicacao_form.save(commit=False)
                medicacao.diagnostico = diagnostico
                medicacao.save()

            return redirect('historico_consultas', paciente_id=paciente.id)

    else:
        diagnostico_form = DiagnosticoForm(instance=diagnostico)
        medicacao_form = MedicacaoForm()

    return render(request, 'benessere/med_atendimento.html', {
        'consulta': consulta,
        'paciente': paciente,
        'diagnostico_form': diagnostico_form,
        'medicacao_form': medicacao_form
    })

@group_required('Medico')
def med_historico_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    consultas = paciente.consultas.all()  # Acessa todas as consultas do paciente
    return render(request, 'benessere/med_historico_paciente.html', {'paciente': paciente, 'consultas': consultas})

@group_required('Medico')  # Use o decorador de grupo, se aplicável
def historico_consultas(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    consultas = paciente.consultas.all()  # Assumindo que `related_name='consultas'` está configurado
    
    return render(request, 'benessere/med_historico_consultas.html', {
        'paciente': paciente,
        'consultas': consultas
    })

@group_required('Gestor')
def gestor_dashboard(request):
    if not request.user.is_authenticated or not request.user.groups.filter(name='Gestor').exists():
        return render(request, '403.html', status=403)

    # Obter todos os usuários cadastrados
    usuarios = User.objects.all()
    
    return render(request, 'benessere/gestor_dashboard.html', {'usuarios': usuarios})

@group_required('Gestor')
def gestor_criar_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            groups = form.cleaned_data['groups']
            
            # Adicionar o usuário aos grupos selecionados
            user.groups.set(groups)
            user.save()

            # Verificar se o usuário é médico e criar o modelo Medico
            if any(group.name == "Medico" for group in groups):
                especialidade = form.cleaned_data['especialidade']
                crm = form.cleaned_data['crm']
                Medico.objects.create(usuario=user, especialidade=especialidade, crm=crm)

            # Redirecionar para o dashboard após a criação do usuário
            return redirect('gestor_dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'benessere/gestor_criar_usuario.html', {'form': form})

@group_required('Gestor')
def gestor_editar_usuario(request, user_id):
    usuario = get_object_or_404(User, pk=user_id)
    grupos = Group.objects.filter(name__in=["Medico", "Gestor", "Recepcionista"])

    if request.method == "POST":
        # Atualiza os dados do usuário
        usuario.username = request.POST.get('username')
        usuario.email = request.POST.get('email')

        # Atualiza o grupo
        grupo_id = request.POST.get('groups')
        if grupo_id:
            grupo = Group.objects.get(pk=grupo_id)
            usuario.groups.clear()  # Limpa grupos anteriores
            usuario.groups.add(grupo)  # Adiciona o novo grupo

        usuario.save()
        return redirect('gestor_dashboard')

    return render(request, 'benessere/gestor_editar_usuario.html', {
        'usuario': usuario,
        'grupos': grupos,
    })

@group_required('Gestor')
def gestor_deletar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('gestor_dashboard')
    
    return render(request, 'benessere/gestor_confirmar_delecao.html', {'user': user})

@group_required('Gestor')
def gestor_unidades(request):
    ufs = Uf.objects.all()
    cidades = Cidade.objects.select_related('uf').all()
    unidades = UnidadeClinica.objects.select_related('cidade', 'cidade__uf').all()
    
    context = {
        'ufs': ufs,
        'cidades': cidades,
        'unidades': unidades,
    }

    return render(request, 'benessere/gestor_unidades.html', context)

@group_required('Gestor')
def gestor_adicionar_unidade(request):
    if request.method == 'POST':
        form = UnidadeClinicaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestor_unidades')  # Redireciona para a página com a lista de unidades
    else:
        form = UnidadeClinicaForm()
    
    return render(request, 'benessere/gestor_adicionar_unidade.html', {'form': form})

@group_required('Gestor')
def gestor_adicionar_unidade(request):
    if request.method == 'POST':
        form = UnidadeClinicaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestor_unidades')  # Redireciona para a lista de unidades
    else:
        form = UnidadeClinicaForm()
    
    return render(request, 'benessere/gestor_adicionar_unidade.html', {'form': form})

@group_required('Gestor')
def gestor_editar_unidade(request, unidade_id):
    # Recupera a unidade clínica a ser editada
    unidade = get_object_or_404(UnidadeClinica, id=unidade_id)

    if request.method == 'POST':
        form = UnidadeClinicaForm(request.POST, instance=unidade)
        if form.is_valid():
            form.save()
            return redirect('gestor_unidades')  # Redireciona para a página com a lista de unidades
    else:
        # Preenche o formulário com os dados da unidade existente
        form = UnidadeClinicaForm(instance=unidade)
    
    return render(request, 'benessere/gestor_editar_unidade.html', {'form': form, 'unidade': unidade})

@group_required('Gestor')
def gestor_deletar_unidade(request, unidade_id):
    unidade = get_object_or_404(UnidadeClinica, id=unidade_id)
    
    if request.method == 'POST':
        unidade.delete()
        return redirect('gestor_unidades')  # Redireciona para a lista de unidades após a exclusão
    
    return render(request, 'benessere/gestor_confirmar_deletar_unidade.html', {'unidade': unidade})
