from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import ConsultaForm, PacienteForm, PagamentoForm # Supondo que você tenha um formulário para consultas
from django.contrib import messages

def recp_lista_consultas(request):
    consultas = Consulta.objects.all()
    return render(request, 'benessere/recp_consultas.html', {'consultas': consultas})

def recp_adicionar_consulta(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('recp_consultas')
    else:
        form = ConsultaForm()

    return render(request, 'benessere/recp_adicionar_consulta.html', {'form': form})


def recp_detalhes_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    checkin_exists = CheckIn.objects.filter(consulta=consulta).exists()
    
    return render(request, 'benessere/recp_detalhes_consulta.html', {
        'consulta': consulta,
        'checkin_exists': checkin_exists
    })

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
    
def remover_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    consulta.delete()
    messages.success(request, 'Consulta removida com sucesso.')
    return redirect('recp_consultas')

def checkin_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    
    # Cria o registro de check-in, se não existir
    checkin, created = CheckIn.objects.get_or_create(consulta=consulta)
    
    if created:
        messages.success(request, 'Check-in realizado com sucesso!')
    else:
        messages.info(request, 'O check-in já foi realizado para esta consulta.')
    
    return redirect('recp_detalhes_consulta', consulta_id=consulta.id)

def desfazer_checkin(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    checkin = CheckIn.objects.filter(consulta=consulta)
    
    if checkin.exists():
        checkin.delete()
        messages.success(request, 'Check-in desfeito com sucesso.')
    else:
        messages.info(request, 'Não há check-in para desfazer.')
    
    return redirect('recp_detalhes_consulta', consulta_id=consulta.id)

def recp_lista_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'benessere/recp_pacientes.html', {'pacientes': pacientes})

def lista_mensagens(request):
    # Aqui você pode adicionar a lógica para buscar mensagens
    mensagens = []  # Exemplo: substitua pelo queryset real, se houver
    return render(request, 'benessere/recp_mensagens.html', {'mensagens': mensagens})

def recp_detalhes_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    consultas = Consulta.objects.filter(paciente=paciente)  # Busca todas as consultas do paciente
    
    return render(request, 'benessere/recp_detalhes_paciente.html', {
        'paciente': paciente,
        'consultas': consultas
    })


def recp_adicionar_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pacientes')
    else:
        form = PacienteForm()
    return render(request, 'benessere/recp_adicionar_paciente.html', {'form': form})

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