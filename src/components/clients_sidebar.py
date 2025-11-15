"""
Sidebar com lista de clientes e botão Novo Cliente
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QInputDialog, QWidgetItem, QHBoxLayout, QLineEdit, QMessageBox
from PySide6.QtCore import Signal, Qt
from typing import List

from src.utils.storage import load_all_clients, create_client, update_client, save_all_clients


class ClientsSidebar(QWidget):
    """Componente lateral com clientes"""
    cliente_selected = Signal(int)
    cliente_created = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_clients()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(10)

        self.btn_new = QPushButton("Novo Cliente")
        self.btn_new.clicked.connect(self.on_new_client)
        self.btn_new.setMinimumHeight(40)
        self.btn_new.setCursor(Qt.PointingHandCursor) # type: ignore
        # estilo similar ao botão Calcular
        self.btn_new.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #28431a, 
                    stop:1 #3d6329
                );
                color: white;
                border-radius: 8px;
                font-size: 13px;
                font-weight: bold;
                padding: 10px 14px;
                border: none;
            }
            QPushButton:hover { opacity: 0.95 }
        """)
        layout.addWidget(self.btn_new)

        self.list_widget = QListWidget()
        self.list_widget.currentRowChanged.connect(self.on_select)
        layout.addWidget(self.list_widget, 1)

        # largura fixa da sidebar para liberar mais espaço à tabela
        self.setFixedWidth(200)

    def load_clients(self):
        self.list_widget.blockSignals(True)
        self.list_widget.clear()
        data = load_all_clients()
        clients = data.get('clients', [])

        for idx, client in enumerate(clients):
            item = QListWidgetItem()

            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(6, 2, 6, 2)
            row_layout.setSpacing(8)

            name_edit = QLineEdit(client.get('name', ''))
            name_edit.setFrame(False)
            name_edit.setStyleSheet('QLineEdit { background: transparent; font-size: 13px; }')
            # associar o item para encontrar a linha depois
            name_edit._list_item = item
            name_edit.editingFinished.connect(lambda ed=name_edit: self.on_name_edited(ed))

            btn_delete = QPushButton('🗑')
            btn_delete.setToolTip('Excluir cliente')
            btn_delete.setFixedSize(26, 26)
            btn_delete.setCursor(Qt.PointingHandCursor)  # type: ignore
            btn_delete.setStyleSheet('QPushButton{ background: transparent; border: none; font-size: 14px; }')
            btn_delete.clicked.connect(lambda _checked, it=item: self.on_delete_clicked(it))

            row_layout.addWidget(name_edit)
            row_layout.addWidget(btn_delete)

            item.setSizeHint(row_widget.sizeHint())
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, row_widget)

        self.list_widget.blockSignals(False)

    def on_new_client(self):
        # Perguntar nome ao usuário
        name, ok = QInputDialog.getText(self, 'Novo Cliente', 'Nome do cliente:')
        if not ok:
            return

        # criar cliente com nome informado
        if name and name.strip():
            client = create_client(name.strip())
        else:
            client = create_client()
        self.load_clients()
        # selecionar último
        last_index = self.list_widget.count() - 1
        self.list_widget.setCurrentRow(last_index)
        self.cliente_created.emit(client)

    def on_name_edited(self, editor: QLineEdit):
        item = getattr(editor, '_list_item', None)
        if item is None:
            return
        row = self.list_widget.row(item)
        try:
            data = load_all_clients()
            clients = data.get('clients', [])
            if 0 <= row < len(clients):
                clients[row]['name'] = editor.text()
                update_client(row, clients[row])
        except Exception:
            pass

    def on_delete_clicked(self, item: QListWidgetItem):
        row = self.list_widget.row(item)
        if row < 0:
            return

        reply = QMessageBox.question(self, 'Confirmar exclusão', f"Excluir cliente '{self.list_widget.item(row).text()}'?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply != QMessageBox.Yes:
            return

        try:
            data = load_all_clients()
            clients = data.get('clients', [])
            if 0 <= row < len(clients):
                clients.pop(row)
                save_all_clients({'clients': clients})
                # recarregar a lista e selecionar próximo item
                self.load_clients()
                new_count = self.list_widget.count()
                new_row = min(row, new_count - 1) if new_count > 0 else -1
                if new_row >= 0:
                    self.list_widget.setCurrentRow(new_row)
                    self.cliente_selected.emit(new_row)
                else:
                    # sem clientes
                    self.cliente_selected.emit(-1)
        except Exception:
            pass

    def on_select(self, idx: int):
        if idx >= 0:
            self.cliente_selected.emit(idx)

    def on_item_changed(self, item: QListWidgetItem):
        """Quando o nome do cliente é alterado na lista, atualizar o storage"""
        row = self.list_widget.row(item)
        try:
            data = load_all_clients()
            clients = data.get('clients', [])
            if 0 <= row < len(clients):
                clients[row]['name'] = item.text()
                update_client(row, clients[row])
        except Exception:
            pass
