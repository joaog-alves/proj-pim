from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import ConsultaForm 

# Create your views here.

def detalhes_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    return render(request, 'detalhes-paciente.html', {'paciente': paciente})

def lista_consultas(request):
    consultas = Consulta.objects.all()
    return render(request, 'consultas.html', {'consultas': consultas})

def criar_consulta(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_consultas')  # Substitua 'lista_consultas' pelo nome da rota desejada após criar a consulta
    else:
        form = ConsultaForm()
    return render(request, 'criar-consulta.html', {'form': form})