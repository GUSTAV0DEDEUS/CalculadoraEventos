from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas # type: ignore
from matplotlib.figure import Figure
from typing import Dict, List, Any


class ChartSectionComponent(QWidget):    
    def __init__(self, cores: List[str], parent=None):
        super().__init__(parent)
        self.cores = cores
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        group = QGroupBox("Visualização Gráfica")
        group.setStyleSheet("""
            QGroupBox {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 12px;
                padding: 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QGroupBox::title {
                color: #28431a;
                subcontrol-origin: margin;
                left: 15px;
                top: 8px;
                padding: 0 5px;
            }
        """)
        
        group_layout = QVBoxLayout()
        group_layout.setContentsMargins(5, 5, 5, 5)
        
        self.figure = Figure(figsize=(7, 5), facecolor='white')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumHeight(400)
        group_layout.addWidget(self.canvas)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        self._criar_grafico_vazio()
    
    def atualizar_grafico(self, payload: Dict[str, Any]):
        """Desenha um gráfico de barras horizontais empilhadas comparando valores esperados vs reais.
        Espera um payload com chaves: 'valores_reais' e 'valores_esperados'.
        """
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        valores_reais = payload.get('valores_reais', {})
        valores_esperados = payload.get('valores_esperados', {})

        labels = list(valores_esperados.keys()) if valores_esperados else list(valores_reais.keys())
        if not labels:
            self._criar_grafico_vazio()
            return

        esperados = [valores_esperados.get(l, 0.0) for l in labels]
        reais = [valores_reais.get(l, 0.0) for l in labels]

        if sum(esperados) == 0 and sum(reais) == 0:
            self._criar_grafico_vazio()
            return

        # Gráfico de barras horizontais empilhadas (melhor visualização)
        y_pos = range(len(labels))
        
        # Calcular percentuais para melhor visualização
        total_esp = sum(esperados) if sum(esperados) > 0 else 1
        total_real = sum(reais) if sum(reais) > 0 else 1
        
        perc_esp = [(e / total_esp) * 100 for e in esperados]
        perc_real = [(r / total_real) * 100 for r in reais]

        # Barras horizontais
        bar_height = 0.35
        
        # Cores em tons de verde - claro para esperado, escuro para real
        cor_esperado = '#70AD47'  # Verde claro
        cor_real = '#3D6329'      # Verde escuro
        
        barras_esp = ax.barh([i - bar_height/2 for i in y_pos], perc_esp, bar_height, 
                             label='Esperado (%)', color=cor_esperado, alpha=0.9)
        barras_real = ax.barh([i + bar_height/2 for i in y_pos], perc_real, bar_height,
                              label='Real (%)', color=cor_real, alpha=0.9)

        ax.set_yticks(list(y_pos))
        ax.set_yticklabels(labels)
        ax.set_xlabel('Percentual (%)')
        ax.set_title('Distribuição: Esperado vs Real', fontsize=13, fontweight='bold', color='#2c3e50')
        ax.legend(loc='lower right')
        ax.grid(axis='x', alpha=0.3, linestyle='--')

        # função auxiliar para formatar percentual
        def fmt_perc(v: float) -> str:
            return f"{v:.1f}%" if v > 0 else ""

        # adicionar labels nas barras
        for bar in barras_esp:
            w = bar.get_width()
            if w > 2:  # só mostrar se >= 2%
                ax.text(w/2, bar.get_y() + bar.get_height()/2, fmt_perc(w),
                       ha='center', va='center', fontsize=9, color='white', fontweight='bold')

        for bar in barras_real:
            w = bar.get_width()
            if w > 2:  # só mostrar se >= 2%
                ax.text(w/2, bar.get_y() + bar.get_height()/2, fmt_perc(w),
                       ha='center', va='center', fontsize=9, color='white', fontweight='bold')

        self.figure.tight_layout()
        self.canvas.draw()
    
    def _criar_grafico_vazio(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        ax.text(
            0.5, 0.5,
            'Aguardando valores...\n\nDigite um valor e clique em Calcular',
            horizontalalignment='center',
            verticalalignment='center',
            transform=ax.transAxes,
            fontsize=12,
            color='#95a5a6',
            style='italic'
        )
        
        ax.axis('off')
        self.figure.tight_layout()
        self.canvas.draw()
    
    def limpar(self):
        self._criar_grafico_vazio()
