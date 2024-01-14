from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from .forms import *
from equipamentos.models import *
import datetime

@user_passes_test(lambda u: u.tipo == 'gestor_infraestrutura', login_url='/accounts/login/')
@login_required
def listaDocumentos(request):
    documentos = Documento.objects.all()
    return render(request, 'documentos/lista.html', {'documentos':documentos})

@user_passes_test(lambda u: u.tipo == 'gestor_infraestrutura', login_url='/accounts/login/')
@login_required
def visualizarDocumento(request, id):
    documento = get_object_or_404(Documento, pk=id)
    return render(request, 'documentos/view.html', {'documento':documento})

@user_passes_test(lambda u: u.tipo == 'gestor_infraestrutura', login_url='/accounts/login/')
@login_required
def inserirDocumento(request):
    if request.method == 'POST':
        form = FormularioDocumento(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/documentos')
    else:
        form = FormularioDocumento()
        return render(request, 'documentos/inserir.html', {'form':form})

@user_passes_test(lambda u: u.tipo == 'gestor_infraestrutura', login_url='/accounts/login/')
@login_required
def editarDocumento(request, id):
    documento = get_object_or_404(Documento, pk=id)
    form = FormularioDocumento(instance=documento)
    if request.method == 'POST':
        form = FormularioDocumento(request.POST, instance=documento)
        if form.is_valid():
            documento.save()
            return redirect('/documentos')
    else:
        return render(request, 'documentos/editar.html', {'documento':documento, 'form':form})

@user_passes_test(lambda u: u.tipo == 'gestor_infraestrutura', login_url='/accounts/login/')
@login_required
def deleteDocumento(request, id):
    documento = get_object_or_404(Documento, pk=id)
    documento.delete()
    return redirect('/documentos')

@user_passes_test(lambda u: u.tipo == 'gestor_infraestrutura', login_url='/accounts/login/')
@login_required
def visualizarDocumentoAutorizacao(request, id):
    documento = get_object_or_404(DocumentoAutorizacao, pk=id)
    lista_escolhas = EscolhaEquipamentoHorario.objects.all()
    context = {
        'documento':documento,
        'lista_escolhas':lista_escolhas
    }
    return render(request, 'documentos/view_autorizacao.html', context)

@user_passes_test(lambda u: u.tipo == 'gestor_infraestrutura', login_url='/accounts/login/')
@login_required
def assinarDocumento(request, id):
    documento = get_object_or_404(DocumentoAutorizacao, pk=id)
    if documento.status == 'aguardando_assinatura':
        documento.status = 'assinado'
        documento.data_inicio = datetime.datetime.now()
        documento.save()
    return redirect(f'/documentos/documento_autorizacao/{documento.id}')