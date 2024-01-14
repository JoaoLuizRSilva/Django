from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import *

class FormularioDocumento(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['nome', 'conteudo']
        widgets = {
            'conteudo': CKEditorWidget(),
        }