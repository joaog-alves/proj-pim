# benessere/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', RedirectView.as_view(url='/login/', permanent=False)),
    path('login/', auth_views.LoginView.as_view(template_name='benessere/login.html'), name='login'),
    path('login_redirect/', views.login_redirect, name='login_redirect'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('acesso-negado/', views.acesso_negado, name='acesso_negado'),
    path('upload_photo/', views.upload_user_photo, name='upload_user_photo'),
    
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
    path('recepcao/pagamentos/adicionar/', views.recp_adicionar_pagamento, name='recp_adicionar_pagamento'),
    path('recepcao/pagamentos/', views.recp_pagamento, name='recp_pagamento'),  # Rota para listar pagamentos
    path('recp_pagamentos/<int:pagamento_id>/', views.recp_detalhes_pagamento, name='recp_detalhes_pagamento'),
    path('recp_pagamentos/<int:pagamento_id>/editar/', views.recp_editar_pagamento, name='recp_editar_pagamento'),

    path('gestor/dashboard/', views.gestor_dashboard, name='gestor_dashboard'),
    path('gestor/usuarios/criar/', views.gestor_criar_usuario, name='gestor_criar_usuario'),
    path('gestor/usuarios/editar/<int:user_id>/', views.gestor_editar_usuario, name='gestor_editar_usuario'),
    path('gestor/unidades/editar/<int:unidade_id>/', views.gestor_editar_unidade, name='gestor_editar_unidade'),
    path('gestor/usuarios/deletar/<int:user_id>/', views.gestor_deletar_usuario, name='gestor_deletar_usuario'),
    path('gestor/unidades/adicionar/', views.gestor_adicionar_unidade, name='gestor_adicionar_unidade'),
    path('gestor/unidades/editar/<int:unidade_id>/', views.gestor_editar_unidade, name='gestor_editar_unidade'),
    path('gestor/unidades/', views.gestor_unidades, name='gestor_unidades'),
    path('gestor/unidades/deletar/<int:unidade_id>/', views.gestor_deletar_unidade, name='gestor_deletar_unidade'),  # Certifique-se que esta linha exista
  
    path('medico/consultas/', views.med_consultas, name='med_consultas'),
    path('medico/consultas/<int:consulta_id>/', views.med_detalhes_consulta, name='med_detalhes_consulta'),
    path('medico/atendimento/<int:consulta_id>/', views.med_atendimento, name='med_atendimento'),
    path('medico/historico/<int:paciente_id>/', views.historico_consultas, name='historico_consultas'),

    path('mensagens/', views.listar_mensagens, name='listar_mensagens'),
    path('mensagens/enviar/', views.enviar_mensagem, name='enviar_mensagem'),
    path('mensagens/enviar/<int:id>/', views.enviar_mensagem, name='enviar_mensagem'),
    path('mensagens/<int:mensagem_id>/', views.ver_mensagem, name='ver_mensagem'),

]