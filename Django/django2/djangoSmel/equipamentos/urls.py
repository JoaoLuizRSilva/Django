from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='lista-equipamentos'),
    path('uso_info/', views.listarRequisicoes, name='uso-info'),
    path('uso_info/edit/<int:id>', views.editarRequisicao),
    path('uso_info/delete/<int:id>', views.deleteUso),
    path('uso_info/<int:id>', views.inserirEscolhas),
    path('uso_info/<int:id1>/delete/<int:id2>', views.deleteHorario),
    path('solicitacao/enviar/<int:id>', views.enviarSolicitacao, name='enviar-solicitacao'),

    path('gestao/equipamentos/', views.gestaoEquipamento, name='gestao-equipamento'),
    path('gestao/equipamentos/requisicao_analogica', views.requisicaoAnalogica, name='requisicao-analogica'),
    path('gestao/equipamentos/tabela', views.tabelaHorarios, name='tabela-horarios'),
    path('gestao/equipamentos/inserir/', views.inserirEquipamento, name='inserir-equipamento'),
    path('gestao/equipamentos/editar/<int:id>', views.editarEquipamento, name='editar-equipamento'),
    path('gestao/equipamentos/delete/<int:id>', views.excluirEquipamento, name='editar-equipamento'),

    path('gestao/solicitacoes', views.listaDeRequisicoes, name='lista-requisicoes'),
    path('gestao/solicitacoes/autorizar/<int:id>', views.autorizarUso, name='autorizar-uso'),
    path('gestao/solicitacoes/autorizar/periodo/<int:id>', views.inserirPeriodo, name='inserir-periodo'),
    path('gestao/solicitacoes/rejeitar/<int:id>', views.rejeitarUso, name='rejeitar-uso'),
    path('gestao/solicitacoes/editar/<int:id>', views.novoHorario, name='novo-horario'),
    path('gestao/solicitacoes/delete/<int:id1>/delete/<int:id2>', views.gestaoDeleteHorario),

    path('gestao/equipamentos/avaliar', views.avaliarEquipamento, name='avaliar-equipamento'),
    path('gestao/equipamentos/avaliacoes', views.listarAvaliacoes, name='lista-avaliacoes'),

    # Dashboard Totais

    path('gestao/dashboard/total_equipamentos', views.totalEquipamentos, name='total-equipamentos'),
    path('gestao/dashboard/total_requisicoes', views.totalRequisicoes, name='total-requisicoes'),
    path('gestao/dashboard/total_requisicoes_pendentes', views.totalRequisicoesPendentes, name='total-requisicoes-pendentes'),
    path('gestao/dashboard/total_requisicoes_autorizadas', views.totalRequisicoesAutorizadas, name='total-requisicoes-autorizadas'),
    path('gestao/dashboard/total_requisicoes_rejeitadas', views.totalRequisicoesRejeitas, name='total-requisicoes-rejeitadas'),
    path('gestao/dashboard/total_equipamentos_danificados', views.totalEquipamentosDanificados, name='total-equipamentos-danificados'),

    # Dashboard Gráficos
    path('gestao/dashboard/relatorio_requisicoes', views.relatorioRequisicoes, name='relatorio-requisicoes'),
    path('gestao/dashboard/relatorio_atualizacao_requisicao', views.relatorioAtualizacaoRequisicoes, name='relatorio-atualizacao-requisicao'),
    path('gestao/dashboard/relatorio_modalidade', views.relatorioModalidade, name='relatorio-modalidade'),
    path('gestao/dashboard/relatorio_genero', views.relatorioGenero, name='relatorio-genero'),
]