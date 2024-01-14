from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from usuarios.forms import CustomUserCreationForm
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Sum, Count 
from datetime import datetime
from django.core.paginator import Paginator
from .models import *
from .forms import *
from documentos.models import *
from documentos.forms import *
# Página de usuário

@login_required
def index(request):
    return render(request, 'equipamentos/equipamentos.html')

@login_required
def listarRequisicoes(request):
    uso_espaco = UsoEspaco.objects.filter(usuario=request.user)

    uso_espaco_paginator = Paginator(uso_espaco, 5)
    page_num = request.GET.get('page')
    page = uso_espaco_paginator.get_page(page_num)

    if request.method == 'POST':
        form = UsoEspacoForm(request.POST)
        if form.is_valid():
            uso_espaco = form.save(commit=False)
            uso_espaco.usuario = request.user
            uso_espaco.situacao = 'rascunho'
            uso_espaco.save()
            return redirect(f'/uso_info/{uso_espaco.id}')
    else:
        uso_espaco_paginator = Paginator(uso_espaco, 5)
        page_num = request.GET.get('page')
        page = uso_espaco_paginator.get_page(page_num)
        form = UsoEspacoForm()
        context = {
            'page':page,
            'form':form,
        }
    return render(request, 'equipamentos/listar_requisicao.html', context)

def deleteUso(request, id):
    uso_espaco = get_object_or_404(UsoEspaco, pk=id)
    if uso_espaco.usuario != request.user:
        return HttpResponseForbidden("Você não tem permissão para acessar esta página.")
    if uso_espaco.situacao == 'rascunho':
        uso_espaco.delete()
    return redirect(f'/uso_info')

@login_required
def inserirEscolhas(request, id):
    uso_espaco = get_object_or_404(UsoEspaco, pk=id)
    if uso_espaco.usuario != request.user:
        return HttpResponseForbidden("Você não tem permissão para acessar esta página.")
    if request.method == 'POST':
        form = EscolhaEquipamentoHorarioForm(request.POST)
        if form.is_valid():
            escolha = form.save(commit=False)
            escolha.uso_espaco = uso_espaco
            escolha.save()
            return redirect(f'/uso_info/{uso_espaco.id}')
    else:
        form = EscolhaEquipamentoHorarioForm()
        escolha = EscolhaEquipamentoHorario.objects.filter(uso_espaco=uso_espaco)
        context = {
            'uso_espaco':uso_espaco,
            'form':form,
            'escolha':escolha
        }
        return render(request, 'equipamentos/nova_escolha.html', context)

def deleteHorario(request, id1, id2):
    uso_espaco = get_object_or_404(UsoEspaco, pk=id1)
    if uso_espaco.usuario != request.user:
        return HttpResponseForbidden("Você não tem permissão para acessar esta página.")
    escolha = get_object_or_404(EscolhaEquipamentoHorario, pk=id2)
    if uso_espaco.usuario != request.user:
        return HttpResponseForbidden("Você não tem permissão para acessar esta página.")
    if uso_espaco.situacao == 'rascunho':
        escolha.delete()
    return redirect(f'/uso_info/{uso_espaco.id}')


@login_required
def enviarSolicitacao(request, id):
    solicitacao = get_object_or_404(UsoEspaco, pk=id)
    if solicitacao.usuario != request.user:
        return HttpResponseForbidden("Você não tem permissão para acessar esta página.")
    if solicitacao.situacao == 'rascunho':
        solicitacao.situacao = 'aguardando'
        solicitacao.save()
    return redirect('/')


# Gestão de equipamentos esportivos
@user_passes_test(lambda u: u.tipo == 'gestor_infraestrutura', login_url='/accounts/login/')
@login_required
def gestaoEquipamento(request):
    equipamentos = Equipamento.objects.all()

    equipamentos_paginator = Paginator(equipamentos, 5)
    page_num = request.GET.get('page')
    page = equipamentos_paginator.get_page(page_num)

    return render(request, 'gestao/equipamentos/equipamentos.html', {'page':page})

def requisicaoAnalogica(request):
    if request.method == 'POST':
        form = UsoEspacoForm(request.POST)
        if form.is_valid():
            uso_espaco = form.save(commit=False)
            uso_espaco.usuario = request.user
            uso_espaco.situacao = 'rascunho'
            uso_espaco.save()
            return redirect(f'/uso_info/{uso_espaco.id}')
    else:
        form = UsoEspacoForm()
        context = {
            'uso_espaco':uso_espaco,
            'form':form
        }
    return render(request, 'equipamentos/listar_requisicao.html', context)


@user_passes_test(lambda u: u.tipo == 'gestor_infraestrutura', login_url='/accounts/login/')
@login_required
def tabelaHorarios(request):
    equipamento_id = request.GET.get('equipamento')
    usuario_id = request.GET.get('usuario')
    modalidade_id = request.GET.get('modalidade')
    atividade_id = request.GET.get('atividade')
    idade_id = request.GET.get('idade')

    escolha_equipamentos = EscolhaEquipamentoHorario.objects.filter(uso_espaco__situacao='autorizado')

    if equipamento_id:
        escolha_equipamentos = escolha_equipamentos.filter(equipamento_id=equipamento_id)

    if usuario_id:
        escolha_equipamentos = escolha_equipamentos.filter(uso_espaco__usuario=usuario_id)

    if modalidade_id:
        escolha_equipamentos = escolha_equipamentos.filter(uso_espaco__tipo_modalidade=modalidade_id)

    if atividade_id:
        escolha_equipamentos = escolha_equipamentos.filter(uso_espaco__tipo_atividade=atividade_id)

    if idade_id:
        escolha_equipamentos = escolha_equipamentos.filter(uso_espaco__publico_alvo=idade_id)

    context = {
        'equipamentos':Equipamento.objects.all(),
        'usuarios':UsuarioCustomizado.objects.all(),
        'modalidades':TipoModalidade.objects.all(),
        'atividades':TipoAtividade.objects.all(),
        'idade': Publico.objects.all(),
        'horarios':[[7, 8], [8, 9], [9, 10], [10, 11], [11, 12], [12, 13], [13, 14], [14, 15], [15, 16], [16, 17], [17, 18], [18, 19], [19, 20], [20, 21], [21, 22]],
        'dias_semana':['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo'],
        'escolha_equipamentos':escolha_equipamentos,
        'uso_espaco': UsoEspaco.objects.all(),
    }
    return render(request, 'gestao/equipamentos/tabela_uso.html', context)


@user_passes_test(lambda u: u.tipo == 'gestor_infraestrutura', login_url='/accounts/login/')
@login_required
def inserirEquipamento(request):
    if request.method == 'POST':
        form = FormularioEquipamento(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/gestao/equipamentos/')
    else:
        form = FormularioEquipamento()
        context = {
            'form':form
        }
    return render(request, 'gestao/equipamentos/inserir.html', context)


@user_passes_test(lambda u: u.tipo == 'gestor_infraestrutura', login_url='/accounts/login/')
@login_required
def editarEquipamento(request, id):
    equipamento = get_object_or_404(Equipamento, pk=id)
    form = FormularioEquipamento(instance=equipamento)
    if request.method == 'POST':
        form = FormularioEquipamento(request.POST, instance=equipamento)
        if form.is_valid():
            equipamento.save()
            return redirect('/gestao/equipamentos/')
    else:
        context = {
            'equipamento':equipamento,
            'form':form
        }
        return render(request, 'gestao/equipamentos/editar.html', context)


@user_passes_test(lambda u: u.tipo == 'gestor_infraestrutura', login_url='/accounts/login/')
@login_required
def excluirEquipamento(request, id):
    equipamento = get_object_or_404(Equipamento, pk=id)
    equipamento.delete()
    return redirect('/gestao/equipamentos/')

@user_passes_test(lambda u: u.tipo == 'gestor_infraestrutura', login_url='/accounts/login/')
@login_required
def listaDeRequisicoes(request):
    lista_de_requisicoes = UsoEspaco.objects.exclude(situacao='rascunho')

    lista_de_requisicoes_paginator = Paginator(lista_de_requisicoes, 5)
    page_num = request.GET.get('page')
    page = lista_de_requisicoes_paginator.get_page(page_num)

    lista_de_escolhas = EscolhaEquipamentoHorario.objects.all()

    documentos = DocumentoAutorizacao.objects.all()
    context = {
        'page':page,
        'lista_de_escolhas':lista_de_escolhas,
        'documentos':documentos,
    }
    return render(request, 'gestao/equipamentos/requisicoes.html', context)

def novoHorario(request, id):
    uso_espaco = get_object_or_404(UsoEspaco, pk=id)
    if request.method == 'POST':
        form = EscolhaEquipamentoHorarioForm(request.POST)
        if form.is_valid():
            escolha = form.save(commit=False)
            escolha.uso_espaco = uso_espaco
            escolha.save()
            return redirect(f'/gestao/solicitacoes/editar/{uso_espaco.id}')
    else:
        form = EscolhaEquipamentoHorarioForm()
        escolha = EscolhaEquipamentoHorario.objects.filter(uso_espaco=uso_espaco)
        context = {
            'uso_espaco':uso_espaco,
            'form':form,
            'escolha':escolha
        }
        return render(request, 'gestao/equipamentos/novo_horario.html', context)
    
def gestaoDeleteHorario(request, id1, id2):
    uso_espaco = get_object_or_404(UsoEspaco, pk=id1)
    escolha = get_object_or_404(EscolhaEquipamentoHorario, pk=id2)
    escolha.delete()
    return redirect(f'/gestao/solicitacoes/editar/{uso_espaco.id}')

@user_passes_test(lambda u: u.tipo == 'gestor_infraestrutura', login_url='/accounts/login/')
@login_required
def autorizarUso(request, id):
    uso_espaco = get_object_or_404(UsoEspaco, pk=id)
    if uso_espaco.situacao == 'aguardando':
        uso_espaco.situacao = 'autorizado'
        documento = DocumentoAutorizacao(info=uso_espaco, status='aguardando_assinatura')
        uso_espaco.save()
        documento.save()
        return redirect(f'/gestao/solicitacoes/autorizar/periodo/{documento.id}')

@user_passes_test(lambda u: u.tipo == 'gestor_infraestrutura', login_url='/accounts/login/')
@login_required
def inserirPeriodo(request, id):
    form = InserirPeriodoForm()
    if request.method == 'POST':
        documento = get_object_or_404(DocumentoAutorizacao, pk=id)
        form = InserirPeriodoForm(request.POST, instance=documento)
        if form.is_valid():
            documento.save()
            usos_espaco = UsoEspaco.objects.all()
            for uso_espaco in usos_espaco:
                if uso_espaco == documento.info:
                    uso_espaco.data_expiracao = documento.data_fim
                    uso_espaco.save()
            return redirect(f'/gestao/solicitacoes')
    else:
        context = {
            'form': form
        }
        return render(request, 'gestao/equipamentos/periodo_documento.html', context)

@user_passes_test(lambda u: u.tipo == 'gestor_infraestrutura', login_url='/accounts/login/')
@login_required
def rejeitarUso(request, id):
    uso_espaco = get_object_or_404(UsoEspaco, pk=id)
    if uso_espaco.situacao == 'aguardando':
        uso_espaco.situacao ='rejeitado'
        uso_espaco.save()
    return redirect('/gestao/solicitacoes')


@user_passes_test(lambda u: u.tipo == 'gestor_infraestrutura', login_url='/accounts/login/')
@login_required
def avaliarEquipamento(request):
    if request.method == 'POST':
        form = FormularioAvaliacao(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.avaliador = request.user
            avaliacao.save()

            equipamento = get_object_or_404(Equipamento, pk=avaliacao.equipamento.id)
            equipamento.condicao_equipamento = avaliacao.condicao_equipamento

            equipamento.save()

            return redirect('/gestao/equipamentos')
    else:
        form = FormularioAvaliacao()
        context = {
            'form':form
        }
    return render(request, 'gestao/equipamentos/avaliar.html', context)


@user_passes_test(lambda u: u.tipo == 'gestor_infraestrutura', login_url='/accounts/login/')
@login_required
def listarAvaliacoes(request):
    avaliacoes = Avaliacao.objects.all()

    avaliacoes_paginator = Paginator(avaliacoes, 5)
    page_num = request.GET.get('page')
    page = avaliacoes_paginator.get_page(page_num)

    context = {
        'page':page
    }
    return render(request, 'gestao/equipamentos/avaliacoes.html', context)


@user_passes_test(lambda u: u.tipo == 'gestor_infraestrutura', login_url='/accounts/login/')
@login_required
def requisicaoAnalogica(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.tipo = 'cidadao'
            user.save()

            uso_espaco = UsoEspaco(usuario=user, estimativa_praticipantes=0, situacao='rascunho', genero_biologico='masc', publico_alvo_id=1, tipo_atividade_id=1, tipo_modalidade_id=1)
            uso_espaco.save()

            return redirect(f'/uso_info/edit/{uso_espaco.id}')
    else:
        form = CustomUserCreationForm()
        context = {
            'form': form
        }
    return render(request, 'registration/resgister-analog.html', context)


def editarRequisicao(request, id):
    uso_espaco = get_object_or_404(UsoEspaco, pk=id)
    if uso_espaco.usuario != request.user:
        return HttpResponseForbidden("Você não tem permissão para acessar esta página.")
    form = UsoEspacoForm(instance=uso_espaco)
    if request.method == 'POST':
        form = UsoEspacoForm(request.POST, instance=uso_espaco)
        if form.is_valid():
            uso_espaco.save()
            return redirect(f'/uso_info/{uso_espaco.id}')
    else:
        context = {
            'form': form
        }
        return render(request, 'gestao/equipamentos/editar_uso.html', context)


# Dahsboard
# Totais
def totalEquipamentos(request):
    total = Equipamento.objects.all().aggregate(Count('id'))['id__count']
    print(total)
    return JsonResponse({'total':total})

def totalRequisicoes(request):
    total = UsoEspaco.objects.exclude(situacao='rascunho').aggregate(Count('id'))['id__count']
    print(total)
    return JsonResponse({'total':total})

def totalRequisicoesPendentes(request):
    total = UsoEspaco.objects.filter(situacao='aguardando').aggregate(Count('id'))['id__count']
    print(total)
    return JsonResponse({'total':total})

def totalRequisicoesAutorizadas(request):
    total = UsoEspaco.objects.filter(situacao='autorizado').aggregate(Count('id'))['id__count']
    print(total)
    return JsonResponse({'total':total})

def totalRequisicoesRejeitas(request):
    total = UsoEspaco.objects.filter(situacao='rejeitado').aggregate(Count('id'))['id__count']
    print(total)
    return JsonResponse({'total':total})

def totalEquipamentosDanificados(request):
    total = Equipamento.objects.filter(condicao_equipamento='pessimo').aggregate(Count('id'))['id__count']
    print(total)
    return JsonResponse({'total':total})

# Gráficos
def relatorioRequisicoes(request):
    x = UsoEspaco.objects.exclude(situacao='rascunho')

    meses = ['Jan', 'Jev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

    data = []
    labels = []
    cont = 0
    mes = datetime.now().month + 1
    ano = datetime.now().year

    for i in range(12):
        mes -= 1
        if mes == 0:
            mes = 12
            ano -= 1

        y = 0
        for i in x:
            if i.data_requisicao.month == mes and i.data_requisicao.year == ano:
                y += 1
        labels.append(meses[mes-1])
        data.append(y)
        cont += 1

    data_json = {'data':data[::-1], 'labels':labels[::-1]}

    return JsonResponse(data_json)

def relatorioAtualizacaoRequisicoes(request):
    x = UsoEspaco.objects.exclude(situacao='rascunho')

    meses = ['Jan', 'Jev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

    data = []
    labels = []
    cont = 0
    mes = datetime.now().month + 1
    ano = datetime.now().year

    for i in range(12):
        mes -= 1
        if mes == 0:
            mes = 12
            ano -= 1

        y = 0
        for i in x:
            if i.data_atualizacao.month == mes and i.data_atualizacao.year == ano:
                y += 1
        labels.append(meses[mes-1])
        data.append(y)
        cont += 1

    data_json = {'data':data[::-1], 'labels':labels[::-1]}

    return JsonResponse(data_json)

def relatorioModalidade(request):
    modalidades = TipoModalidade.objects.all()
    label = []
    data = []
    for modalidade in modalidades:
        total = UsoEspaco.objects.filter(tipo_modalidade=modalidade)
        total = len(total)
        label.append(modalidade.nome)
        data.append(total)

    x = list(zip(label, data))
    x.sort(key=lambda x: x[1], reverse=True)
    x = list(zip(*x))

    return JsonResponse({'labels': x[0][:10], 'data': x[1][:10]})

def relatorioGenero(request):
    generos = [['masc', 'Masculino'], ['fem', 'Feminino'], ['mis', 'Misto']]
    label = []
    data = []
    for genero in generos:
        total = UsoEspaco.objects.filter(genero_biologico=genero[0])
        total = len(total)
        label.append(genero[1])
        data.append(total)

    x = list(zip(label, data))
    x = list(zip(*x))
    return JsonResponse({'labels': x[0][:3], 'data': x[1][:3]})