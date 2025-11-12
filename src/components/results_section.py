from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QGroupBox
from PySide6.QtCore import Qt
from typing import Dict


class ResultsSectionComponent(QWidget):
    
    def __init__(self, percentuais: Dict[str, float], parent=None):
        super().__init__(parent)
        self.percentuais = percentuais
        self.labels_valores = {}
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        group = QGroupBox("Distribuição de Valores")
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
                color: #667eea;
                subcontrol-origin: margin;
                left: 15px;
                top: 8px;
                padding: 0 5px;
            }
        """)
        
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)
        grid_layout.setContentsMargins(10, 10, 10, 10)
        
        row = 0
        for categoria, percentual in self.percentuais.items():
            label_cat = QLabel(f"{categoria} ({percentual}%):")
            label_cat.setStyleSheet("""
                QLabel {
                    color: #495057;
                    font-size: 13px;
                    font-weight: normal;
                }
            """)
            
            label_valor = QLabel("R$ 0,00")
            label_valor.setStyleSheet("""
                QLabel {
                    color: #667eea;
                    font-size: 14px;
                    font-weight: bold;
                }
            """)
            
            grid_layout.addWidget(label_cat, row, 0, Qt.AlignLeft) # type: ignore
            grid_layout.addWidget(label_valor, row, 1, Qt.AlignRight) # type: ignore
            
            self.labels_valores[categoria] = label_valor
            row += 1
        
        divisor = QLabel()
        divisor.setFixedHeight(2)
        divisor.setStyleSheet("QLabel { background-color: #e0e0e0; }")
        grid_layout.addWidget(divisor, row, 0, 1, 2)
        row += 1
        
        label_total_text = QLabel("Total:")
        label_total_text.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 15px;
                font-weight: bold;
            }
        """)
        
        self.label_total_valor = QLabel("R$ 0,00")
        self.label_total_valor.setStyleSheet("""
            QLabel {
                color: #2ecc71;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        
        grid_layout.addWidget(label_total_text, row, 0, Qt.AlignLeft) # type: ignore
        grid_layout.addWidget(self.label_total_valor, row, 1, Qt.AlignRight) # type: ignore
        
        group.setLayout(grid_layout)
        layout.addWidget(group)
    
    def atualizar_valores(self, valores: Dict[str, float], total: float):
        for categoria, valor in valores.items():
            if categoria in self.labels_valores:
                valor_formatado = self._formatar_moeda(valor)
                self.labels_valores[categoria].setText(valor_formatado)
        
        self.label_total_valor.setText(self._formatar_moeda(total))
    
    def limpar(self):
        for label in self.labels_valores.values():
            label.setText("R$ 0,00")
        self.label_total_valor.setText("R$ 0,00")
    
    @staticmethod
    def _formatar_moeda(valor: float) -> str:
        return f"R$ {valor:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')