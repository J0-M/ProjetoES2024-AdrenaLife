from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    #path('getCategorias', views.getCategoriasAtividades, name='getAllCategorias'), #pagina que retorna todas as categorias
    #path('categoria/<str:name>', views.getCategoriaByName, name='getCategoria'),
    path('', views.init_aplicacao, name='inicio'),  # Tela de login como página inicial
    path('padrao/', views.home, name='padrao'), 
    
    path('eventos/listar/', views.listar_eventos, name='listar_eventos'),
    path('criar_usuario/', views.criar_usuario, name='criar_usuario'),
    path('perfil/', views.perfil, name='perfil'),
    path('alterar_senha/', views.alterar_senha, name='alterar_senha'),
    path('excluir_conta/', views.excluir_conta, name='excluir_conta'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('categorias/', views.categoriaManager, name='categoriaManager'),# Sempre necessário tem / depois de categorias
    path('atividades/', views.atividadeManager, name='attManager'),
    path('eventos/', views.eventoManager, name='eventoManager'),
    
    path('inscricao/', views.inscricaoManager, name='inscricao')
]