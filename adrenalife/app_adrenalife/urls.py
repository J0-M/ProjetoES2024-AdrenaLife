from django.urls import path, include
from django.contrib import admin

from . import views

urlpatterns = [
    #path('getCategorias', views.getCategoriasAtividades, name='getAllCategorias'), #pagina que retorna todas as categorias
    #path('categoria/<str:name>', views.getCategoriaByName, name='getCategoria'),
    path('categorias/', views.categoriaManager, name='categoriaManager'),# Sempre necessário tem / depois de categorias
    path('atividades/', views.atividadeManager, name='attManager'),
    path('eventos/', views.eventoManager, name='eventoManager')
]