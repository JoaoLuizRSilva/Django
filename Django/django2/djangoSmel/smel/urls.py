from django.contrib import admin
from django.urls import path, include

# Define as URLs do projeto
urlpatterns = [
    # URL da página de administração do Django
    path('admin/', admin.site.urls),
    
    # URL da página principal do projeto
    path('', include('equipamentos.urls')),
    
    # URLs relacionadas ao sistema de contas dos usuários
    path('accounts/', include('usuarios.urls')),
    
    # URLs relacionadas à autenticação de usuários
    path('accounts/', include('django.contrib.auth.urls')),

    path('documentos/', include('documentos.urls')),
]