PERCENTUAIS = {
    'Staff': 12.0,
    'Locação': 9.0,
    'CMV': 30.0,
    'Nota': 12.0,
    'Lucro': 37.0
}

CORES = ['#28431a', '#3d6329', '#52833a', '#6ba34b', '#84c35c']

ESTILOS = {
    'header': """
        QWidget {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #28431a, 
                stop:1 #3d6329
            );
            border-radius: 15px;
            padding: 25px;
        }
    """,
    
    'titulo': """
        QLabel {
            color: white;
            font-size: 28px;
            font-weight: bold;
            background: transparent;
        }
    """,
    
    'subtitulo': """
        QLabel {
            color: rgba(255, 255, 255, 0.9);
            font-size: 14px;
            background: transparent;
        }
    """,
    
    'input_group': """
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
            padding: 0 5px;
        }
    """,
    
    'input_field': """
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
    """,
    
    'btn_calcular': """
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
                stop:0 #3a5c28, 
                stop:1 #2f4a1f
            );
        }
        QPushButton:pressed {
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #264414, 
                stop:1 #1f3510
            );
        }
    """,
    
    'results_group': """
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
            padding: 0 5px;
        }
    """,
    
    'chart_group': """
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
            padding: 0 5px;
        }
    """,
    
    'label_categoria': """
        QLabel {
            color: #495057;
            font-size: 13px;
            font-weight: normal;
        }
    """,
    
    'label_valor': """
        QLabel {
            color: #28431a;
            font-size: 14px;
            font-weight: bold;
        }
    """,
    
    'label_total': """
        QLabel {
            color: #2ecc71;
            font-size: 16px;
            font-weight: bold;
        }
    """,
    
    'main_window': """
        QMainWindow {
            background-color: #f0f2f5;
        }
    """
}
