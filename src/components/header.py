from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import os


class HeaderComponent(QWidget):    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)
        
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setSpacing(8)
        header_layout.setContentsMargins(25, 25, 25, 25)
        
        logo_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'logo.png')
        if os.path.exists(logo_path):
            logo_label = QLabel()
            pixmap = QPixmap(logo_path)
            scaled_pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation) # type: ignore
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setAlignment(Qt.AlignCenter) # type: ignore
            header_layout.addWidget(logo_label)
        
        titulo = QLabel("Calculadora de Eventos")
        titulo.setAlignment(Qt.AlignCenter) # type: ignore
        titulo.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 28px;
                font-weight: bold;
                background: transparent;
            }
        """)
        header_layout.addWidget(titulo)
        
        subtitulo = QLabel("Distribuição Inteligente de Custos")
        subtitulo.setAlignment(Qt.AlignCenter) # type: ignore
        subtitulo.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 14px;
                background: transparent;
            }
        """)
        header_layout.addWidget(subtitulo)
        
        header_widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #28431a, 
                    stop:1 #3d6329
                );
                border-radius: 15px;
            }
        """)
        
        layout.addWidget(header_widget)
