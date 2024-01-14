from django.db import models
from ckeditor.fields import RichTextField
from usuarios.models import *

class TipoEquipamento(models.Model):
    nome = models.CharField(max_length=255)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
 
class TipoModalidade(models.Model):
    nome = models.CharField(max_length=255)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
    
class TipoAtividade(models.Model):
    nome = models.CharField(max_length=255)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Cidade(models.Model):
    nome = models.CharField(max_length=100)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
    
class Bairro(models.Model):
    nome = models.CharField(max_length=100)
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Equipamento(models.Model):
    POSSUI = (
        ('possui', 'Possui'),
        ('npossui', 'Não Possui'),
    )

    CONDICAO = (
        ('pessimo', 'Péssimo'),
        ('ruim', 'Ruim'),
        ('bom', 'Bom'),
        ('otimo', 'Ótimo'),
        ('excelente', 'Excelente'),
    )

    nome = models.CharField(max_length=255)
    bairro = models.ForeignKey(Bairro, on_delete=models.CASCADE)
    cep = models.CharField(max_length=8)
    endereco = models.CharField(max_length=255)
    longitude = models.FloatField()
    latitude = models.FloatField()
    tamanho = models.FloatField()
    tipo_equipamento = models.ForeignKey(TipoEquipamento, on_delete=models.CASCADE)
    tipo_modalidade = models.ManyToManyField(TipoModalidade)

    condicao_equipamento = models.CharField(
        max_length=9,
        choices=CONDICAO
    )

    rede_eletrica = models.CharField(
        max_length=7,
        choices=POSSUI,
    )
    rede_hidraulica = models.CharField(
        max_length=7,
        choices=POSSUI,
    )
    banheiro_vestiario = models.CharField(
        max_length=7,
        choices=POSSUI,
    )
    parques_jardins = models.CharField(
        max_length=7,
        choices=POSSUI,
    )
    arquibancada = models.CharField(
        max_length=7,
        choices=POSSUI,
    )
    cobertura = models.CharField(
        max_length=7,
        choices=POSSUI,
    )
    cercamento = models.CharField(
        max_length=7,
        choices=POSSUI,
    )
    grama_sintetica = models.CharField(
        max_length=7,
        choices=POSSUI,
    )

    foto_aerea = models.ImageField()
    fotos = models.ImageField()


    def __str__(self):
        return self.nome

class Avaliacao(models.Model):
    STATUS = (
        ('muitobaixa', 'Muito Baixa'),
        ('baixa', 'Baixa'),
        ('regular', 'Regular'),
        ('alta', 'Alta'),
        ('muitoalta', 'Muito Alta'),
    )

    CONDICAO = (
        ('pessimo', 'Péssimo'),
        ('ruim', 'Ruim'),
        ('bom', 'Bom'),
        ('otimo', 'Ótimo'),
        ('excelente', 'Excelente'),
    )

    avaliador = models.ForeignKey(UsuarioCustomizado, on_delete=models.CASCADE)
    data_avaliacao = models.DateTimeField(auto_now_add=True)
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE)
    assunto = models.CharField(max_length=100)
    descricao_condicao = models.TextField()
    condicao_equipamento = models.CharField(
        max_length=9,
        choices=CONDICAO
    )

    
    eletrica = models.CharField(
        max_length=10,
        choices=STATUS
    )
    hidraulica = models.CharField(
        max_length=10,
        choices=STATUS
    )
    serralheria = models.CharField(
        max_length=10,
        choices=STATUS
    )
    carpintaria = models.CharField(
        max_length=10,
        choices=STATUS
    )
    alvenaria = models.CharField(
        max_length=10,
        choices=STATUS
    )
    vidracaria = models.CharField(
        max_length=10,
        choices=STATUS
    )
    limpeza = models.CharField(
        max_length=10,
        choices=STATUS
    )
    pintura = models.CharField(
        max_length=10,
        choices=STATUS
    )
    jardinagem = models.CharField(
        max_length=10,
        choices=STATUS
    )


class Publico(models.Model):
    faixa_idade = models.CharField(max_length=12)

    def __str__(self):
        return self.faixa_idade

class UsoEspaco(models.Model):
    STATUS = (
        ('rascunho', 'Rascunho'),
        ('aguardando', 'Aguardando Resposta'),
        ('autorizado', 'Autorizado'),
        ('rejeitado', 'Rejeitado'),
    )

    GENERO = (
        ('masc', 'Masculino'),
        ('fem', 'Feminino'),
        ('mis', 'Misto'),
    )


    usuario = models.ForeignKey(UsuarioCustomizado, on_delete=models.CASCADE)
    data_requisicao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    situacao = models.CharField(
        max_length=10,
        choices=STATUS,
    )

    genero_biologico = models.CharField(
        max_length=4,
        choices=GENERO,
    )

    publico_alvo = models.ForeignKey(Publico, on_delete=models.DO_NOTHING)

    estimativa_praticipantes = models.IntegerField()

    tipo_atividade = models.ForeignKey(TipoAtividade, on_delete=models.CASCADE)
    tipo_modalidade = models.ForeignKey(TipoModalidade, on_delete=models.CASCADE)

    data_expiracao = models.DateField(null=True)

    def situacao_text(self):
        return dict(UsoEspaco.STATUS)[self.situacao]
    
    def genero_text(self):
        return dict(UsoEspaco.GENERO)[self.genero_biologico]
    
    
class EscolhaEquipamentoHorario(models.Model):

    DIA = (
        ('segunda', 'Segunda-Feira'),
        ('terca', 'Terça-Feira'),
        ('quarta', 'Quarta-Feira'),
        ('quinta', 'Quinta-Feira'),
        ('sexta', 'Sexta-Feira'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
    )

    uso_espaco = models.ForeignKey(UsoEspaco, on_delete=models.CASCADE)

    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE)

    dia = models.CharField(
        max_length=7,
        choices=DIA
    )
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()

    def dia_semana(self):
        return dict(EscolhaEquipamentoHorario.DIA)[self.dia]