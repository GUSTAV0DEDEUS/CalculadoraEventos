import sys
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt

from src.components import (
    HeaderComponent, 
    InputSectionComponent, 
    ResultsSectionComponent, 
    ChartSectionComponent
)
from src.utils import PERCENTUAIS, CORES, CalculadoraCustos


class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("T2F Calculador de eventos")
        self.setMinimumSize(1000, 750)
        
        self.calculadora = CalculadoraCustos(PERCENTUAIS)
        
        self.setup_ui()
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
        """)
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(25, 25, 25, 25)
        
        self.header = HeaderComponent()
        main_layout.addWidget(self.header)
        
        self.input_section = InputSectionComponent()
        self.input_section.calcular_clicked.connect(self.on_calcular)
        main_layout.addWidget(self.input_section)
        
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)
        
        self.results_section = ResultsSectionComponent(PERCENTUAIS)
        content_layout.addWidget(self.results_section, 1)
        
        self.chart_section = ChartSectionComponent(CORES)
        content_layout.addWidget(self.chart_section, 2)
        
        main_layout.addLayout(content_layout)
    
    def on_calcular(self, valor_total: float):
        try:
            valores = self.calculadora.calcular(valor_total)
            
            self.results_section.atualizar_valores(valores, valor_total)
            
            self.chart_section.atualizar_grafico(valores)
            
        except ValueError as e:
            print(f"Erro ao calcular: {e}")
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        
        
__all__ = [
    'MainWindow'
]
