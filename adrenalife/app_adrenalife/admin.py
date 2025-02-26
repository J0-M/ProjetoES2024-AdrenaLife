from django.contrib import admin

from .models import Usuario

from .models import categoria_atividade

admin.site.register(categoria_atividade)

admin.site.register(Usuario)

# Register your models here.
