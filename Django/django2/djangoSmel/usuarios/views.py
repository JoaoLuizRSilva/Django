from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm

# Define a função de visualização "register" que processa o registro de um novo usuário.
# Se a requisição HTTP for um POST, os dados do formulário são validados e, se válidos, um novo usuário é criado e autenticado.
# Se a requisição HTTP for um GET, um formulário vazio é exibido para o usuário preencher.
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.tipo = 'cidadao' # Define o tipo de usuário como "cidadao" (pode ser modificado de acordo com as necessidades do seu aplicativo).
            user.save()
            login(request, user) # Autentica o usuário no sistema após o registro.
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})