# benessere/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('recepcao/consultas/', views.recp_lista_consultas, name='recp_consultas'),
    path('recepcao/consultas/adicionar/', views.recp_adicionar_consulta, name='recp_adicionar_consulta'),  # Adicione a URL para adicionar consultas
    path('recepcao/consultas/<int:consulta_id>/', views.recp_detalhes_consulta, name='recp_detalhes_consulta'),  # Altere para consulta_id
    path('recepcao/consultas/<int:consulta_id>/editar/', views.recp_editar_consulta, name='recp_editar_consulta'),
    path('recepcao/consultas/<int:consulta_id>/remover/', views.remover_consulta, name='remover_consulta'),
    path('recepcao/consultas/<int:consulta_id>/checkin/', views.checkin_consulta, name='checkin_consulta'),
    path('recepcao/consultas/<int:consulta_id>/desfazer_checkin/', views.desfazer_checkin, name='desfazer_checkin'),  # URL para desfazer check-in
    path('recepcao/pacientes/', views.recp_lista_pacientes, name='recp_pacientes'),
    path('recepcao/pacientes/adicionar/', views.recp_adicionar_paciente, name='recp_adicionar_paciente'),
    path('recepcao/pacientes/<int:paciente_id>/', views.recp_detalhes_paciente, name='recp_detalhes_paciente'),
    path('recepcao/pacientes/<int:paciente_id>/editar/', views.recp_editar_paciente, name='recp_editar_paciente'),  # URL para editar paciente
    path('mensagens/', views.lista_mensagens, name='recp_mensagens'),
]
