from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton, QGroupBox
from PySide6.QtCore import Qt, Signal
import re


class InputSectionComponent(QWidget):
    calcular_clicked = Signal(float)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._formatando = False
        self.setup_ui()
    
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        group = QGroupBox("Valor do Evento")
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
        
        group_layout = QHBoxLayout()
        group_layout.setSpacing(15)
        
        label = QLabel("Valor Total (R$):")
        label.setStyleSheet("QLabel { font-size: 13px; color: #495057; }")
        
        self.input_valor = QLineEdit()
        self.input_valor.setPlaceholderText("Digite o valor do evento (ex: 10.000,00)")
        self.input_valor.setMinimumHeight(45)
        self.input_valor.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px 15px;
                font-size: 16px;
                background-color: #f8f9fa;
            }
            QLineEdit:focus {
                border: 2px solid #28431a;
                background-color: white;
            }
        """)
        
        self.input_valor.textChanged.connect(self._formatar_input)
        self.input_valor.returnPressed.connect(self._on_calcular)
        
        self.btn_calcular = QPushButton("Calcular")
        self.btn_calcular.setMinimumHeight(45)
        self.btn_calcular.setMinimumWidth(130)
        self.btn_calcular.setCursor(Qt.PointingHandCursor) # type: ignore
        self.btn_calcular.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #28431a, 
                    stop:1 #3d6329
                );
                color: white;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                padding: 12px 30px;
                border: none;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5568d3, 
                    stop:1 #6a3f8f
                );
            }
            QPushButton:pressed {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a5abc, 
                    stop:1 #5c3680
                );
            }
        """)
        self.btn_calcular.clicked.connect(self._on_calcular)
        
        group_layout.addWidget(label)
        group_layout.addWidget(self.input_valor, 1)
        group_layout.addWidget(self.btn_calcular)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
    
    def _formatar_input(self, texto: str):
        if self._formatando:
            return
        
        self._formatando = True
        
        cursor_pos = self.input_valor.cursorPosition()
        
        texto_limpo = re.sub(r'[^\d,.]', '', texto)
        
        partes = texto_limpo.replace(',', '.').split('.')
        
        if len(partes) > 2:
            parte_inteira = ''.join(partes[:-1])
            parte_decimal = partes[-1]
        elif len(partes) == 2:
            parte_inteira = partes[0]
            parte_decimal = partes[1]
        else:
            parte_inteira = partes[0]
            parte_decimal = ''
        
        if parte_decimal:
            parte_decimal = parte_decimal[:2]
        
        if parte_inteira:
            parte_inteira = str(int(parte_inteira)) if parte_inteira else '0'
            parte_inteira_formatada = f"{int(parte_inteira):,}".replace(',', '.')
        else:
            parte_inteira_formatada = ''
        
        if parte_decimal:
            texto_formatado = f"{parte_inteira_formatada},{parte_decimal}"
        elif texto_limpo.endswith(',') or texto_limpo.endswith('.'):
            texto_formatado = f"{parte_inteira_formatada},"
        else:
            texto_formatado = parte_inteira_formatada
        
        if texto_formatado != texto:
            diff = len(texto_formatado) - len(texto)
            nova_pos = cursor_pos + diff
            
            self.input_valor.setText(texto_formatado)
            self.input_valor.setCursorPosition(min(nova_pos, len(texto_formatado)))
        
        self._formatando = False
    
    def _on_calcular(self):
        try:
            valor_str = self.input_valor.text().replace('.', '').replace(',', '.')
            if not valor_str:
                return
            
            valor_total = float(valor_str)
            if valor_total > 0:
                self.calcular_clicked.emit(valor_total)
        except ValueError:
            pass
    
    def get_valor(self) -> float:
        try:
            valor_str = self.input_valor.text().replace('.', '').replace(',', '.')
            return float(valor_str) if valor_str else 0.0
        except ValueError:
            return 0.0
    
    def clear(self):
        self.input_valor.clear()
