from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas # type: ignore
from matplotlib.figure import Figure
from typing import Dict, List


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
        group_layout.addWidget(self.canvas)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        self._criar_grafico_vazio()
    
    def atualizar_grafico(self, valores: Dict[str, float]):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        labels = list(valores.keys())
        sizes = list(valores.values())
        
        if sum(sizes) == 0:
            self._criar_grafico_vazio()
            return
        
        wedges, texts, autotexts = ax.pie( # type: ignore
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            startangle=90,
            colors=self.cores[:len(labels)],
            textprops={'fontsize': 10, 'color': '#2c3e50'},
            pctdistance=0.75
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
        
        for text in texts:
            text.set_fontsize(9)
            text.set_fontweight('semibold')
        
        ax.axis('equal')
        
        ax.set_title(
            'Distribuição de Custos',
            fontsize=13,
            fontweight='bold',
            pad=15,
            color='#2c3e50'
        )
        
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
