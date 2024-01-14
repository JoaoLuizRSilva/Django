from django.contrib import admin
from .models import *

# Registra o modelo UsuarioCustomizado no painel de administração do Django.
admin.site.register(UsuarioCustomizado)