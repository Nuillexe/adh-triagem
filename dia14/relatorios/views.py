
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db import transaction

from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from formulario.models import Paciente, Evento, Medical_measurement
from .services import gerar_estatisticas


NOME_EVENTO = 'dia14-Ação social de Educação em diabetes'


def obter_evento():
    return get_object_or_404(Evento, nome=NOME_EVENTO)


@login_required(login_url='login')
def painel_relatorio(request):

    evento = obter_evento()
    context = gerar_estatisticas(evento)

    return render(request, "relatorios/relatorios.html", context)


@login_required(login_url='login')
def deletar_participante(request, paciente_id):

    paciente = get_object_or_404(Paciente, pk=paciente_id)

    if request.method == 'POST':
        with transaction.atomic():
            # Remove as medições vinculadas ao paciente
            Medical_measurement.objects.filter(
                paciente=paciente
            ).delete()

            # Depois remove o paciente
            paciente.delete()

        messages.success(
            request,
            "Paciente e suas medições foram deletados com sucesso!"
        )

    return redirect('relatorios')


@login_required(login_url='login')
def gerar_relatorio_pdf(request):

    evento = obter_evento()
    estatisticas = gerar_estatisticas(evento)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        'attachment; filename="relatorio_adh_conquista.pdf"'
    )

    doc = SimpleDocTemplate(
        response,
        pagesize=letter,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    elementos = []

    # Estilos
    styles = getSampleStyleSheet()

    estilo_titulo = ParagraphStyle(
        'Titulo',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#0056b3'),
        alignment=1,
        spaceAfter=6
    )

    estilo_subtitulo = ParagraphStyle(
        'Subtitulo',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#555555'),
        alignment=1,
        spaceAfter=15
    )

    estilo_secao = ParagraphStyle(
        'Secao',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#333333'),
        spaceBefore=10,
        spaceAfter=6
    )

    estilo_celula = ParagraphStyle(
        'Celula',
        parent=styles['Normal'],
        fontSize=8,
        leading=10
    )

    estilo_cabecalho = ParagraphStyle(
        'Cabecalho',
        parent=estilo_celula,
        textColor=colors.white,
        fontName='Helvetica-Bold'
    )

    # Cabeçalho do relatório
    elementos.append(
        Paragraph("<b>ADH CONQUISTA</b>", estilo_titulo)
    )

    elementos.append(
        Paragraph(
            "Ação Comunitária de Educação e Conscientização sobre o Diabetes",
            estilo_subtitulo
        )
    )

    elementos.append(
        Paragraph("<b>Relatório de Atendimentos e Triagem</b>", estilo_secao)
    )

    elementos.append(
        Paragraph(f"Evento: {evento.nome}", styles['Normal'])
    )

    elementos.append(
        Paragraph(
            f"Data do evento: {evento.data.strftime('%d/%m/%Y')}",
            styles['Normal']
        )
    )

    elementos.append(
        Paragraph(f"Descrição: {evento.descricao}", styles['Normal'])
    )

    elementos.append(Spacer(1, 15))

    # Resumo estatístico
    elementos.append(
        Paragraph("<b>1. Resumo Estatístico</b>", estilo_secao)
    )

    dados_estatisticos = [
        ["Indicador", "Resultado"],
        [
            "Total de pacientes atendidos",
            str(estatisticas['total_participantes'])
        ],
        ["Pacientes com DM1", f"{estatisticas['porc_dm1']}%"],
        ["Pacientes com DM2", f"{estatisticas['porc_dm2']}%"],
        ["Pacientes com hipertensão", f"{estatisticas['porc_ht']}%"],
        ["Pacientes sem condição informada", f"{estatisticas['porc_nenhum']}%"],
        ["DM1 associados à hipertensão", f"{estatisticas['porc_ht_dm1']}%"],
        ["DM2 associados à hipertensão", f"{estatisticas['porc_ht_dm2']}%"],
        ["Glicemia elevada", f"{estatisticas['porc_glicemia_alta']}%"],
        ["Pressão arterial elevada", f"{estatisticas['porc_pressao_alta']}%"],
    ]

    tabela_stats = Table(
        dados_estatisticos,
        colWidths=[350, 120]
    )

    tabela_stats.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0056b3')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [
            colors.white,
            colors.HexColor('#f2f2f2')
        ]),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))

    elementos.append(tabela_stats)
    elementos.append(Spacer(1, 15))

    # Listagem de pacientes e medições
    elementos.append(
        Paragraph("<b>2. Listagem de Pacientes</b>", estilo_secao)
    )

    tabela_dados = [[
        Paragraph("Nome", estilo_cabecalho),
        Paragraph("Idade", estilo_cabecalho),
        Paragraph("Glicemia", estilo_cabecalho),
        Paragraph("Pressão", estilo_cabecalho),
        Paragraph("Condição", estilo_cabecalho)
    ]]

    medicoes = estatisticas['medicoes'].order_by('-criado_em')

    for medicao in medicoes:

        paciente = medicao.paciente

        nome = paciente.nome
        idade = str(paciente.idade)
        glicemia = f"{medicao.glicemia} mg/dL"
        pressao = medicao.pressao_arterial_str()
        status = paciente.condicao_saude

        tabela_dados.append([
            Paragraph(nome, estilo_celula),
            Paragraph(idade, estilo_celula),
            Paragraph(glicemia, estilo_celula),
            Paragraph(pressao, estilo_celula),
            Paragraph(status, estilo_celula)
        ])

    tabela_pacientes = Table(
        tabela_dados,
        colWidths=[170, 40, 75, 65, 120],
        repeatRows=1
    )

    tabela_pacientes.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0056b3')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dddddd')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [
            colors.white,
            colors.HexColor('#f2f2f2')
        ]),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))

    elementos.append(tabela_pacientes)

    # Geração do PDF
    doc.build(elementos)

    return response
