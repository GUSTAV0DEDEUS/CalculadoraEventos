"""
Módulo para exportar relatórios de eventos em PDF
"""
import os
from datetime import datetime
from typing import Dict, Optional
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas as pdfcanvas
import matplotlib
matplotlib.use('Agg')  # Backend sem GUI
import matplotlib.pyplot as plt
from io import BytesIO


def format_brl(valor: float) -> str:
    """Formata valor em reais"""
    return f"R$ {valor:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')


def create_chart_image(valores_esperados: Dict[str, float], valores_reais: Dict[str, float], chart_type='bar'):
    """Cria gráfico e retorna como imagem em bytes"""
    fig, ax = plt.subplots(figsize=(6, 3), facecolor='white')
    
    labels = list(valores_esperados.keys())
    esperados = [valores_esperados.get(l, 0.0) for l in labels]
    reais = [valores_reais.get(l, 0.0) for l in labels]
    
    if chart_type == 'bar':
        # Gráfico de barras horizontais com percentuais
        total_esp = sum(esperados) if sum(esperados) > 0 else 1
        total_real = sum(reais) if sum(reais) > 0 else 1
        
        perc_esp = [(e / total_esp) * 100 for e in esperados]
        perc_real = [(r / total_real) * 100 for r in reais]
        
        y_pos = range(len(labels))
        bar_height = 0.35
        
        cores_esp = ['#28431a', '#3d6329', '#4a7a31', '#5a8f3a', '#6ba543']
        ax.barh([i - bar_height/2 for i in y_pos], perc_esp, bar_height, 
                label='Esperado', color=cores_esp[:len(labels)], alpha=0.9)
        ax.barh([i + bar_height/2 for i in y_pos], perc_real, bar_height,
                label='Real', color='#63c76a', alpha=0.9)
        
        ax.set_yticks(list(y_pos))
        ax.set_yticklabels(labels, fontsize=8)
        ax.set_xlabel('Percentual (%)', fontsize=9)
        ax.set_title('Distribuição: Esperado vs Real', fontsize=10, fontweight='bold', color='#2c3e50')
        ax.legend(loc='lower right', fontsize=8)
        ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    
    # Salvar em buffer
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    
    return buf


def create_profit_chart(valores_reais: Dict[str, float]):
    """Cria gráfico de pizza mostrando lucro vs custos"""
    fig, ax = plt.subplots(figsize=(4, 4), facecolor='white')
    
    lucro = valores_reais.get('Lucro', 0.0)
    total_custos = sum([v for k, v in valores_reais.items() if k != 'Lucro'])
    
    if lucro + total_custos > 0:
        valores = [lucro, total_custos]
        labels_pie = ['Lucro', 'Custos Totais']
        cores_pie = ['#4a7a31', '#e74c3c']
        
        wedges, texts, autotexts = ax.pie(valores, labels=labels_pie, autopct='%1.1f%%',
                                           colors=cores_pie, startangle=90,
                                           textprops={'fontsize': 9})
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax.set_title('Lucro vs Custos', fontsize=10, fontweight='bold', pad=10)
    else:
        ax.text(0.5, 0.5, 'Sem dados', ha='center', va='center', fontsize=10, color='gray')
        ax.axis('off')
    
    plt.tight_layout()
    
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    
    return buf


def draw_header_on_canvas(canvas_obj, doc, client_name: str, date_str: str, logo_path: Optional[str]):
    """Desenha o header verde diretamente no canvas, ignorando margens"""
    canvas_obj.saveState()
    
    # Dimensões
    page_width = A4[0]
    page_height = A4[1]
    header_height = 35*mm
    radius = 8
    
    # Posição do header (no topo da página)
    header_y = page_height - header_height
    
    # Desenhar retângulo verde com bordas arredondadas
    canvas_obj.setFillColor(colors.HexColor('#28431a'))
    canvas_obj.setStrokeColor(colors.HexColor('#28431a'))
    
    # Desenhar retângulo com bordas arredondadas
    canvas_obj.roundRect(0, header_y, page_width, header_height, radius, 
                        stroke=0, fill=1)
    
    # Corrigir cantos superiores (fazer quadrados)
    canvas_obj.rect(0, page_height - radius, radius, radius, stroke=0, fill=1)
    canvas_obj.rect(page_width - radius, page_height - radius, radius, radius, stroke=0, fill=1)
    
    # Adicionar logo se existir
    # Logo alinhada com a margem esquerda do conteúdo (20mm)
    logo_x = 20*mm
    logo_y = header_y + (header_height / 2) - (21*mm / 2)
    
    if logo_path and os.path.exists(logo_path):
        try:
            # Tentar carregar a imagem
            canvas_obj.drawImage(logo_path, logo_x, logo_y, 
                           width=21*mm, height=21*mm, 
                           preserveAspectRatio=True, mask='auto')
            text_x = logo_x + 21*mm + 8
            print(f"Logo carregada com sucesso: {logo_path}")
        except Exception as e:
            print(f"Erro ao carregar logo {logo_path}: {e}")
            # Tentar sem o mask='auto'
            try:
                canvas_obj.drawImage(logo_path, logo_x, logo_y, 
                               width=21*mm, height=21*mm, 
                               preserveAspectRatio=True)
                text_x = logo_x + 21*mm + 8
                print(f"Logo carregada sem mask")
            except Exception as e2:
                print(f"Erro ao carregar logo (segunda tentativa): {e2}")
                text_x = 20*mm
    else:
        print(f"Logo não encontrada ou caminho inválido: {logo_path}")
        text_x = 20*mm
    
    # Adicionar texto (nome e data)
    canvas_obj.setFillColor(colors.white)
    
    # Nome do cliente (bold)
    canvas_obj.setFont('Helvetica-Bold', 18)
    canvas_obj.drawString(text_x, header_y + (header_height / 2) + 6, client_name)
    
    # Data (normal)
    canvas_obj.setFont('Helvetica', 11)
    canvas_obj.drawString(text_x, header_y + (header_height / 2) - 10, date_str)
    
    canvas_obj.restoreState()


def export_client_to_pdf(client_data: Dict, output_path: str):
    """Exporta dados do cliente para PDF"""
    
    # Preparar dados do header - tentar múltiplos nomes de logo
    base_path = os.path.join(os.path.dirname(__file__), '..', '..')
    logo_candidates = ['logo.png', 't2f.png', 'Logo.png', 'LOGO.png']
    logo_path = None
    
    for logo_name in logo_candidates:
        candidate_path = os.path.join(base_path, logo_name)
        if os.path.exists(candidate_path):
            logo_path = candidate_path
            print(f"Logo encontrada: {candidate_path}")
            break
    
    if logo_path is None:
        print(f"Nenhuma logo encontrada em {base_path}")
        print(f"Arquivos disponíveis: {os.listdir(base_path) if os.path.exists(base_path) else 'diretório não existe'}")
    
    data_atual = datetime.now().strftime('%d/%m/%Y')
    client_name = client_data.get('name', 'Cliente')
    
    # Função de callback para desenhar header em cada página
    def add_header(canvas_obj, doc):
        draw_header_on_canvas(canvas_obj, doc, client_name, data_atual, logo_path)
    
    # Criar documento com margens normais
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                           topMargin=40*mm,  # Espaço para o header
                           bottomMargin=15*mm,
                           leftMargin=20*mm, 
                           rightMargin=20*mm)
    
    story = []
    styles = getSampleStyleSheet()
    
    # Estilo customizado
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#3d6329'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6
    )
    
    # Não adicionar header na story - será desenhado pelo callback
    # Apenas adicionar espaçador para compensar o header
    
    # Subtítulo do relatório
    story.append(Paragraph(f"<b>Relatório de Evento</b>", subtitle_style))
    story.append(Spacer(1, 5*mm))
    
    # Valor total
    valor_total = client_data.get('valor_total', 0.0)
    story.append(Paragraph(f"<b>Valor Total do Evento:</b> {format_brl(valor_total)}", normal_style))
    
    # Calcular dados de lucro para exibir logo abaixo
    percentuais = client_data.get('percentuais', {})
    valores_reais = client_data.get('valores_reais', {})
    valores_esperados = {k: valor_total * (v / 100) for k, v in percentuais.items()}
    
    lucro_real = valores_reais.get('Lucro', 0.0)
    lucro_esperado = valores_esperados.get('Lucro', 0.0)
    lucro_diff = lucro_real - lucro_esperado
    
    # Adicionar informações de lucro
    story.append(Paragraph(f"<b>Lucro Esperado:</b> {format_brl(lucro_esperado)}", normal_style))
    story.append(Paragraph(f"<b>Lucro Real:</b> {format_brl(lucro_real)}", normal_style))
    
    if lucro_diff > 0:
        story.append(Paragraph(f"<b>Variação:</b> <font color='green'>+{format_brl(lucro_diff)} (acima do esperado)</font>", normal_style))
    elif lucro_diff < 0:
        story.append(Paragraph(f"<b>Variação:</b> <font color='red'>{format_brl(lucro_diff)} (abaixo do esperado)</font>", normal_style))
    else:
        story.append(Paragraph(f"<b>Variação:</b> Conforme planejado", normal_style))
    
    story.append(Spacer(1, 5*mm))
    
    # Tabela de valores detalhados
    story.append(Paragraph("<b>Detalhamento de Custos e Margens</b>", subtitle_style))
    
    percentuais = client_data.get('percentuais', {})
    valores_reais = client_data.get('valores_reais', {})
    
    # Preparar dados da tabela
    table_data = [['Categoria', 'Margem (%)', 'Valor Esperado', 'Valor Real', 'Diferença']]
    
    total_real = sum(valores_reais.values())
    
    for categoria in percentuais.keys():
        perc = percentuais[categoria]
        esp = valores_esperados.get(categoria, 0.0)
        real = valores_reais.get(categoria, 0.0)
        diff = real - esp
        diff_str = format_brl(diff)
        if diff > 0:
            diff_str = f"+{diff_str}"
        
        table_data.append([
            categoria,
            f"{perc:.1f}%",
            format_brl(esp),
            format_brl(real),
            diff_str
        ])
    
    # Totais
    total_esp = sum(valores_esperados.values())
    total_diff = total_real - total_esp
    total_diff_str = format_brl(total_diff)
    if total_diff > 0:
        total_diff_str = f"+{total_diff_str}"
    
    table_data.append([
        'TOTAL',
        '100%',
        format_brl(total_esp),
        format_brl(total_real),
        total_diff_str
    ])
    
    # Criar tabela estilizada
    table = Table(table_data, colWidths=[35*mm, 25*mm, 35*mm, 35*mm, 30*mm])
    table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#28431a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        
        # Corpo
        ('BACKGROUND', (0, 1), (-1, -2), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -2), 0.5, colors.HexColor('#e0e0e0')),
        
        # Linha de zebra
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#f8f9fa')]),
        
        # Linha de total
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#3d6329')),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('LINEABOVE', (0, -1), (-1, -1), 2, colors.HexColor('#28431a')),
        ('TOPPADDING', (0, -1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 8),
    ]))
    
    story.append(table)
    story.append(Spacer(1, 10*mm))
    
    # Gráficos
    story.append(Paragraph("<b>Visualizações Gráficas</b>", subtitle_style))
    story.append(Spacer(1, 3*mm))
    
    # Gráfico de distribuição
    chart_buf = create_chart_image(valores_esperados, valores_reais)
    chart_img = Image(chart_buf, width=160*mm, height=60*mm)
    story.append(chart_img)
    story.append(Spacer(1, 5*mm))
    
    # Gráfico de lucro
    profit_buf = create_profit_chart(valores_reais)
    profit_img = Image(profit_buf, width=80*mm, height=80*mm)
    
    profit_table = Table([[profit_img]], colWidths=[80*mm])
    profit_table.setStyle(TableStyle([('ALIGN', (0, 0), (0, 0), 'CENTER')]))
    story.append(profit_table)
    
    # Rodapé
    story.append(Spacer(1, 10*mm))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.gray,
        alignment=TA_CENTER
    )
    story.append(Paragraph(f"Relatório gerado em {data_atual} - Calculadora de Eventos", footer_style))
    
    # Construir PDF com callbacks de header
    doc.build(story, onFirstPage=add_header, onLaterPages=add_header)
    
    return output_path
