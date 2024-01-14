from django.db import models
from django.contrib.auth.models import AbstractUser

# Cria um modelo de usuário personalizado que herda do modelo de usuário padrão do Django.
# O modelo personalizado adiciona um campo "tipo" para distinguir se o usuário é um cidadão comum ou um gestor de infraestrutura, 
# e um campo "telefone_contato" para armazenar o número de telefone do usuário.
class UsuarioCustomizado(AbstractUser):
    CATEGORIA = (
        ('cidadao', 'Cidadão'),
        ('gestor_infraestrutura', 'Gestor de Infraestrutura'),
        ('gestor_eventos', 'Gestor de Eventos'),
    )

    tipo = models.CharField(
        max_length=21,
        choices=CATEGORIA,
    )
    telefone_contato = models.CharField(max_length=11)