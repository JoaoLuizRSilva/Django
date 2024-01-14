from django.db import models
from equipamentos.models import *
from ckeditor.fields import RichTextField

class Documento(models.Model):
    nome = models.CharField(max_length=255)
    conteudo = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.nome

class DocumentoAutorizacao(models.Model):
    STATUS = (
        ('aguardando_assinatura', 'Aguardando assinatura'),
        ('assinado', 'Assinado'),
    )

    info = models.ForeignKey(UsoEspaco, on_delete=models.DO_NOTHING)
    status = models.CharField(
        max_length=21,
        choices=STATUS,
    )
    
    data_inicio = models.DateField(null=True)
    data_fim = models.DateField(null=True)