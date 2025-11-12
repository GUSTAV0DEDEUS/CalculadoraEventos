import sys
import os
from pathlib import Path 
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from src import MainWindow

def main():
    app = QApplication(sys.argv)

    app.setApplicationName('T2F Calculador de eventos')

    app.setStyle('Fusion')

    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS  # type: ignore
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    icon_path = os.path.join(base_path, 'icon.ico')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
