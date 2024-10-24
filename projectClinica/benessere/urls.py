# benessere/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='benessere/login.html'), name='login'),
    path('login_redirect/', views.login_redirect, name='login_redirect'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('criar_usuario/', views.criar_usuario, name='criar_usuario'),
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
    path('medico/consultas/', views.med_consultas, name='med_consultas'),
    path('medico/mensagens/', views.med_mensagens, name='med_mensagens'),  
    path('medico/consultas/<int:consulta_id>/', views.med_detalhes_consulta, name='med_detalhes_consulta'),
    path('mensagens/', views.lista_mensagens, name='recp_mensagens'),
]
