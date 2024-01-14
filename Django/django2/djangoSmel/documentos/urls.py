from django.urls import path
from . import views

urlpatterns = [
    # path('', views.listaDocumentos, name='lista-documentos'),
    # path('view/<int:id>', views.visualizarDocumento, name='visualizar-documento'),
    # path('inserir', views.inserirDocumento, name='inserir-documento'),
    # path('editar/<int:id>', views.editarDocumento, name='editar-documento'),
    # path('delete/<int:id>', views.deleteDocumento, name='delete-documento'),

    path('documento_autorizacao/<int:id>', views.visualizarDocumentoAutorizacao, name='visualizar-documento-autorizacao'),
    path('documento_autorizacao/assinatura/<int:id>', views.assinarDocumento, name='assinar-documento'),
]