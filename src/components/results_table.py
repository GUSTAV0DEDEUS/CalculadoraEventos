"""
Tabela editável para substituir o gráfico de pizza
Exibe percentuais iniciais, valores esperados e campos editáveis para valores reais
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QStyledItemDelegate, QLineEdit
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDoubleValidator
from typing import Dict
import re


def format_brl(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')


class MoneyDelegate(QStyledItemDelegate):
    """Delegate para edição de valores monetários com máscara dinâmica (milhares + vírgula)"""
    def createEditor(self, parent, option, index):
        # Mostrar o prefixo R$ já no editor para o usuário enquanto edita.
        editor = QLineEdit(parent)
        editor.setPlaceholderText('R$ 0,00')
        editor.setAlignment(Qt.AlignRight)
        return editor

    def setEditorData(self, editor, index):
        text = index.model().data(index)
        if text is None:
            text = ''
        # manter o texto formatado (ex: R$ 1.234,56) no editor para melhor UX
        editor.setText(text)

    def setModelData(self, editor, model, index):
        text = editor.text()
        # aceitar entradas com ou sem 'R$' e com '.' milhares e ',' decimal
        raw = re.sub(r"[^0-9,\.]", '', text)
        # transformar em formato python decimal (ponto)
        raw = raw.replace('.', '').replace(',', '.')
        try:
            val = float(raw) if raw else 0.0
        except Exception:
            val = 0.0

        # formatar para BRL na célula
        model.setData(index, format_brl(val))



class ResultsTableComponent(QWidget):
    dados_alterados = Signal(dict)

    def __init__(self, percentuais: Dict[str, float], parent=None):
        super().__init__(parent)
        self.percentuais = percentuais
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Categoria', 'Percentual (%)', 'Valor Esperado', 'Valor Real', 'Percentual Real (%)'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # estilo do cabeçalho (verde) para combinar com header do app
        self.table.setStyleSheet("QHeaderView::section{ background-color: #28431a; color: white; padding: 6px; font-weight: bold; }")
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.AllEditTriggers)
        # conectar sinais
        self.table.cellChanged.connect(self.on_cell_changed)

        # Delegate para editar valores reais
        self.money_delegate = MoneyDelegate()
        # Valor Real é coluna 3
        self.table.setItemDelegateForColumn(3, self.money_delegate)

        layout.addWidget(self.table)

    def load_data(self, percentuais: Dict[str, float], valor_total: float, valores_reais: Dict[str, float]):
        self.table.blockSignals(True)
        # armazenar para uso no gráfico: valores esperados por categoria
        self.last_percentuais = percentuais
        categorias = list(percentuais.keys())
        self.table.setRowCount(len(categorias))

        # calcular valores esperados
        valores_esperados = {c: valor_total * (percentuais[c] / 100) for c in categorias}
        self.last_valores_esperados = valores_esperados

        for row, categoria in enumerate(categorias):
            # Categoria
            item_cat = QTableWidgetItem(categoria)
            item_cat.setFlags(item_cat.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(row, 0, item_cat)

            # Percentual inicial (formatado)
            perc_text = f"{percentuais[categoria]:.0f}%" if abs(percentuais[categoria] - round(percentuais[categoria])) < 0.005 else f"{percentuais[categoria]:.2f}%"
            item_perc = QTableWidgetItem(perc_text)
            item_perc.setFlags(item_perc.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(row, 1, item_perc)

            # Valor esperado (formatado como R$)
            item_esp = QTableWidgetItem(f"R$ {valores_esperados[categoria]:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))
            item_esp.setFlags(item_esp.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(row, 2, item_esp)

            # Valor real (editável) - exibir em R$
            val_real = valores_reais.get(categoria, 0.0) if valores_reais is not None else 0.0
            item_real = QTableWidgetItem(f"R$ {val_real:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))
            self.table.setItem(row, 3, item_real)

            # Percentual real (calculado)
            total_reais = sum(valores_reais.values()) if valores_reais and sum(valores_reais.values()) > 0 else 0.0
            perc_real = (val_real / total_reais) * 100 if total_reais > 0 else 0.0
            # Formatar percentual real: sem casas se inteiro, com 2 casas se decimal
            perc_text_real = f"{perc_real:.0f}%" if abs(perc_real - round(perc_real)) < 0.005 else f"{perc_real:.2f}%"
            item_perc_real = QTableWidgetItem(perc_text_real)
            item_perc_real.setFlags(item_perc_real.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(row, 4, item_perc_real)

        self.table.blockSignals(False)

    def on_cell_changed(self, row: int, column: int):
        # Apenas reagir se coluna de Valor Real foi alterada
        if column != 3:
            return

        categorias = []
        valores_reais = {}
        for r in range(self.table.rowCount()):
            item_cat = self.table.item(r, 0)
            item_val = self.table.item(r, 3)
            if item_cat is None:
                continue
            cat = item_cat.text()
            categorias.append(cat)

            text = item_val.text() if item_val is not None else ''
            # Permitir entrada formatada com R$ e pontos e vírgulas
            try:
                val = float(text.replace('R$', '').replace('.', '').replace(',', '.').strip()) if text else 0.0
            except Exception:
                val = 0.0
            valores_reais[cat] = val

        total_real = sum(valores_reais.values())
        # Atualizar percentuais reais
        for r, cat in enumerate(categorias):
            perc_real = (valores_reais.get(cat, 0.0) / total_real) * 100 if total_real > 0 else 0.0
            perc_text_real = f"{perc_real:.0f}%" if abs(perc_real - round(perc_real)) < 0.005 else f"{perc_real:.2f}%"
            self.table.blockSignals(True)
            self.table.setItem(r, 4, QTableWidgetItem(perc_text_real))
            self.table.blockSignals(False)

        # Emitir sinal com dados atualizados
        # incluir também percentuais e valores esperados para que o gráfico compare
        payload = {
            'valores_reais': valores_reais,
            'total_real': total_real,
            'percentuais': getattr(self, 'last_percentuais', {}),
            'valores_esperados': getattr(self, 'last_valores_esperados', {})
        }
        self.dados_alterados.emit(payload)
