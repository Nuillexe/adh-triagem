from django.shortcuts import render, redirect
from formulario.models import Participate
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from formulario.models import Participate  # Certifique-se de importar o seu model
from .services import gerar_estatisticas

@login_required(login_url='login')
def painel_relatorio(request):
    
    context=gerar_estatisticas()

    return render(request, "relatorios/relatorios.html", context)


@login_required(login_url='login')
def deletar_participante(request, participante_id):

    p=Participate.objects.get(id=participante_id)
    p.delete()
    messages.success(request, "Participante deletado com sucesso!")
    return redirect('relatorios') 


@login_required(login_url='login')
def gerar_relatorio_pdf(request):
    # 1. Configura a resposta HTTP para o navegador entender que é um PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_adh_conquista.pdf"'

    # 2. Configura o documento (margens, tamanho da página)
    doc = SimpleDocTemplate(response, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elementos = []

    # 3. Estilos de texto
    styles = getSampleStyleSheet()
    estilo_titulo = ParagraphStyle(
        'Titulo',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#0056b3'),
        alignment=1, # Centralizado
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

    # --- CABEÇALHO ---
    elementos.append(Paragraph("<b>ADH CONQUISTA</b>", estilo_titulo))
    elementos.append(Paragraph("Ação Comunitária de Educação e Conscientização sobre o Diabetes", estilo_subtitulo))
    elementos.append(Paragraph("<b>Relatório Geral de Atendimentos e Triagem</b>", estilo_secao))
    elementos.append(Paragraph("Data de Emissão: 14/11/2026", styles['Normal']))
    elementos.append(Spacer(1, 15))

    # --- 1. RESUMO ESTATÍSTICO (Buscando dados reais do banco) ---
    estatisticas= gerar_estatisticas()
    
    elementos.append(Paragraph("<b>1. Resumo Estatístico</b>", estilo_secao))
    
    dados_estatisticos = [
        [Paragraph(f"• Total de Atendidos: {estatisticas['total_participantes']}", styles['Normal'])],
        [Paragraph(f"• Somente Dm1: {estatisticas['porc_dm1']}", styles['Normal'])],
        [Paragraph(f"• Somente Dm2: {estatisticas['porc_dm2']}", styles['Normal'])],
        [Paragraph(f"• Hipertensos e DM1: {estatisticas['porc_ht_dm1']}", styles['Normal'])],
        [Paragraph(f"• Hipertensos e DM2: {estatisticas['porc_ht_dm2']}", styles['Normal'])],
    ]
    tabela_stats = Table(dados_estatisticos, colWidths=[500])
    tabela_stats.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f9f9f9')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
    ]))
    elementos.append(tabela_stats)
    elementos.append(Spacer(1, 15))

    # --- 2. LISTAGEM DE PACIENTES ---
    elementos.append(Paragraph("<b>2. Listagem de Pacientes</b>", estilo_secao))
    
    # Cabeçalho da Tabela
    tabela_dados = [["Nome", "Idade" ,"Glicemia", "Pressão", "Status"]]
    
    # Pega os participantes cadastrados no banco
    participantes = Participate.objects.all().order_by('-id')
    
    for p in participantes:
        # Formata os valores de acordo com os campos reais do seu model Participate
        nome = getattr(p, 'nome', 'N/D')
        idade= getattr(p,'idade', 'N/D' )
        glicemia = f"{getattr(p, 'glicemia', 'N/D')} mg/dL"
        pressao = f"{getattr(p, 'pressaoAlta', '0')}/{getattr(p, 'pressaoBaixa', '0')}"
        status = getattr(p, 'condicao_saude', 'N/D')
        
        tabela_dados.append([nome, idade ,glicemia, pressao, status])

    # Monta a tabela no ReportLab
    tabela_pacientes = Table(tabela_dados, colWidths=[180, 50, 100, 100, 120])
    tabela_pacientes.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0056b3')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#ffffff')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f2f2f2')]),
    ]))
    
    elementos.append(tabela_pacientes)

    # 4. Constrói o PDF e envia
    doc.build(elementos)
    return response
