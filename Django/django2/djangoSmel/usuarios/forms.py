from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UsuarioCustomizado

# Define um formulário personalizado de criação de usuário que herda do formulário de criação de usuário padrão do Django.
# O formulário personalizado adiciona um campo "telefone_contato" para que os usuários possam fornecer um número de telefone durante o registro.
class CustomUserCreationForm(UserCreationForm):
    telefone_contato = forms.CharField(max_length=11)

    class Meta:
        model = UsuarioCustomizado
        # Adiciona os campos do formulário personalizado ao conjunto de campos do formulário de criação de usuário padrão do Django.
        fields = UserCreationForm.Meta.fields + ('telefone_contato', 'username', 'password1', 'password2')
