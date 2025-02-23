
from django.urls import path, include
from app_adrenalife import views
from django.contrib import admin

urlpatterns = [
    #rota, view responsável, nome de referência
    #rota é "adrenalife.com"
    path('admin/', admin.site.urls), # abre a pagina de admin para cadastrar objetos
    path('',views.home,name='home'), # home do site
    path('cadastro_evento',views.cadastro_evento,name='cadastro_evento'),
    path('cadastro_atividades', views.cadastro_atividades, name='cadastro_atividades'),
    
    path('apiCategorias/', include('app_adrenalife.urls'), name='api_urls'), # /api/(url) # links relacionados a api
    path('categoria_atividades/', views.categoria_atividades, name='categoria_atividades')
]