import sys
from pathlib import Path 
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from src import MainWindow

def main():
    app = QApplication(sys.argv)

    app.setApplicationName('T2F Calculador de eventos')

    app.setStyle('Fusion')

    icon_tmp = str(Path('icon.ico'))
    if icon_tmp:
        app.setWindowIcon(QIcon(icon_tmp))

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
