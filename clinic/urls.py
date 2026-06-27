from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('pacientes/', views.pacientes, name='pacientes'),
    path('pacientes/adicionar/', views.paciente_add, name='paciente_add'),
    path('pacientes/exportar/', views.pacientes_export, name='pacientes_export'),
    path('agenda/', views.agenda, name='agenda'),
    path('agenda/novo/', views.agenda_add, name='agenda_add'),
    path('prontuarios/', views.prontuarios, name='prontuarios'),
    path('prontuarios/novo/', views.prontuario_add, name='prontuario_add'),
    path('estoque/', views.estoque, name='estoque'),
    path('estoque/novo/', views.estoque_add, name='estoque_add'),
    path('estoque/relatorio/', views.estoque_relatorio, name='estoque_relatorio'),
    path('financeiro/', views.financeiro, name='financeiro'),
    path('financeiro/novo/', views.financeiro_add, name='financeiro_add'),
    path('financeiro/relatorio/', views.financeiro_relatorio, name='financeiro_relatorio'),
    path('relatorios/', views.relatorios, name='relatorios'),
    path('relatorios/gerar/', views.relatorio_add, name='relatorio_add'),
    path('administracao/', views.administracao, name='administracao'),
    path('administracao/adicionar/', views.administracao_add, name='administracao_add'),
    path('administracao/permissoes/', views.administracao_permissoes, name='administracao_permissoes'),
    path('check-pages/', views.check_pages, name='check_pages'),
]
