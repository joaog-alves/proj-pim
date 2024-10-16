from django.urls import path
from . import views

urlpatterns = [
    path('paciente/<int:paciente_id>/', views.detalhes_paciente, name='detalhes_paciente'),
    path('consultas/', views.lista_consultas, name='lista_consultas'),
    path('consulta/criar/', views.criar_consulta, name='criar_consulta'),
    path('consulta/<int:consulta_id>/', views.detalhes_consulta, name='detalhes_consulta'),
]
