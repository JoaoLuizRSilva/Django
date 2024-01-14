from django.forms import ModelForm
from django import forms
from .models import *
from documentos.models import *

class FormularioEquipamento(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = ['nome', 'bairro', 'cep', 'endereco', 'longitude', 'latitude', 'tamanho', 'tipo_equipamento', 'tipo_modalidade', 'rede_eletrica', 'rede_hidraulica', 'banheiro_vestiario', 'parques_jardins', 'arquibancada', 'cobertura', 'cercamento', 'grama_sintetica']
        
    tipo_modalidade = forms.ModelMultipleChoiceField(
        queryset=TipoModalidade.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

class FormularioAvaliacao(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['equipamento', 'assunto', 'descricao_condicao', 'condicao_equipamento', 'eletrica', 'hidraulica', 'serralheria', 'carpintaria', 'alvenaria', 'vidracaria', 'limpeza', 'pintura', 'jardinagem']

class UsoEspacoForm(forms.ModelForm):
    class Meta:
        model = UsoEspaco
        fields = ['tipo_atividade', 'tipo_modalidade', 'genero_biologico', 'publico_alvo', 'estimativa_praticipantes']

class EscolhaEquipamentoHorarioForm(forms.ModelForm):
    class Meta:
        model = EscolhaEquipamentoHorario
        fields = ['equipamento', 'dia', 'horario_inicio', 'horario_fim']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['horario_inicio'].widget = forms.TimeInput(attrs={'type': 'time'})
        self.fields['horario_fim'].widget = forms.TimeInput(attrs={'type': 'time'})

class InserirPeriodoForm(forms.ModelForm):
    class Meta:
        model = DocumentoAutorizacao
        fields = ['data_fim']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_fim'].widget = forms.DateInput(attrs={'type': 'date'})