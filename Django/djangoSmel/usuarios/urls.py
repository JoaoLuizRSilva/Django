from django.urls import path
from . import views

# Define a rota "register/" que é mapeada para a função "register" no arquivo "views.py" deste aplicativo.
# A rota é nomeada como "user-register" e pode ser referenciada em outros lugares do aplicativo, como em arquivos de template HTML.
urlpatterns = [
    path('register/', views.register, name='user-register'),
]