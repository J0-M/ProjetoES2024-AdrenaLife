
from django.urls import path
from app_adrenalife import views
from django.contrib import admin

urlpatterns = [
    #rota, view responsável, nome de referência
    #rota é "adrenalife.com"
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),

]