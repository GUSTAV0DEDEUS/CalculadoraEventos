import sys
from typing import Dict

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt

from src.components.header import HeaderComponent
from src.components.input_section import InputSectionComponent
from src.components.clients_sidebar import ClientsSidebar
from src.components.results_table import ResultsTableComponent
from src.components.chart_section import ChartSectionComponent
from src.utils.storage import load_all_clients, update_client, get_client, create_client
from src.utils.constants import PERCENTUAIS, CORES
from src.utils.calculator import CalculadoraCustos


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora de Eventos")
        self.setMinimumSize(1200, 850)  # Aumentado para dar mais espaço à tabela

        # Estado
        self.clients_data = load_all_clients()
        self.current_client_index = 0 if self.clients_data.get('clients') else -1

        # Calculadora padrão usada para cálculos iniciais
        self.calculadora = CalculadoraCustos(PERCENTUAIS)

        self.setup_ui()

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
        """)

        # Se já houver cliente, carregar
        if self.current_client_index >= 0:
            self.load_client(self.current_client_index)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(12)

        # Sidebar de clientes
        self.sidebar = ClientsSidebar()
        self.sidebar.cliente_selected.connect(self.on_client_selected)
        self.sidebar.cliente_created.connect(self.on_client_created)
        main_layout.addWidget(self.sidebar, 0)

        # Área principal vertical
        area = QVBoxLayout()

        self.header = HeaderComponent()
        area.addWidget(self.header)

        self.input_section = InputSectionComponent()
        self.input_section.calcular_clicked.connect(self.on_calcular)
        area.addWidget(self.input_section)

        # Results table (mais espaço vertical para evitar overflow)
        self.results_table = ResultsTableComponent(PERCENTUAIS)
        self.results_table.dados_alterados.connect(self.on_dados_alterados)
        area.addWidget(self.results_table)

        # Chart abaixo da tabela (menos espaço que a tabela)
        self.chart_section = ChartSectionComponent(CORES)
        area.addWidget(self.chart_section, 1)

        # conectar sinal para atualizar gráfico quando dados da tabela mudarem
        self.results_table.dados_alterados.connect(lambda payload: self.chart_section.atualizar_grafico(payload))

        main_layout.addLayout(area, 1)

    def on_client_selected(self, index: int):
        self.current_client_index = index
        self.load_client(index)

    def on_client_created(self, client_data: Dict):
        # selecionar último
        self.current_client_index = len(load_all_clients().get('clients', [])) - 1
        self.load_client(self.current_client_index)

    def load_client(self, index: int):
        try:
            client = get_client(index)
        except Exception:
            return

        # Carregar percentuais, valor_total e valores_reais
        percentuais = client.get('percentuais', PERCENTUAIS)
        valor_total = client.get('valor_total', 0.0)
        valores_reais = client.get('valores_reais', {k: 0.0 for k in percentuais.keys()})

        # Atualizar UI
        self.input_section.input_valor.setText(f"{valor_total:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))
        self.results_table.load_data(percentuais, valor_total, valores_reais)
        # atualizar gráfico com valores esperados + reais
        try:
            payload = {
                'valores_reais': valores_reais,
                'valores_esperados': {k: valor_total * (percentuais[k] / 100) for k in percentuais.keys()}
            }
            self.chart_section.atualizar_grafico(payload)
        except Exception:
            pass

    def on_calcular(self, valor_total: float):
        # Recalcular valores esperados e salvar no cliente atual
        if self.current_client_index < 0:
            # Criar cliente padrão se nenhum existe
            create_client('Cliente 1')
            self.sidebar.load_clients()
            self.current_client_index = len(load_all_clients().get('clients', [])) - 1

        data = load_all_clients()
        clients = data.get('clients', [])
        client = clients[self.current_client_index]
        client['valor_total'] = valor_total

        # Calcular valores esperados
        for cat, perc in client.get('percentuais', PERCENTUAIS).items():
            # atualizar valores_reais somente se estiverem zerados
            if 'valores_reais' not in client:
                client['valores_reais'] = {k: 0.0 for k in client['percentuais'].keys()}
            # não sobrescrever valores_reais aqui

        # Salvar
        update_client(self.current_client_index, client)

        # Atualizar tabela
        self.results_table.load_data(client.get('percentuais', PERCENTUAIS), valor_total, client.get('valores_reais', {}))
        try:
            payload = {
                'valores_reais': client.get('valores_reais', {}),
                'valores_esperados': {k: valor_total * (client.get('percentuais', {}).get(k, 0.0) / 100) for k in client.get('percentuais', {}).keys()}
            }
            self.chart_section.atualizar_grafico(payload)
        except Exception:
            pass

    def on_dados_alterados(self, payload: Dict):
        # Atualizar dados do cliente no storage
        if self.current_client_index < 0:
            return

        data = load_all_clients()
        client = data['clients'][self.current_client_index]
        client['valores_reais'] = payload.get('valores_reais', client.get('valores_reais', {}))
        client['ultimo_total_real'] = payload.get('total_real', 0.0)
        update_client(self.current_client_index, client)
        # também atualizar gráfico com payload completo
        try:
            esperados = payload.get('valores_esperados') or {k: client.get('valor_total', 0.0) * (client.get('percentuais', {}).get(k, 0.0) / 100) for k in client.get('percentuais', {}).keys()}
            self.chart_section.atualizar_grafico({'valores_reais': client['valores_reais'], 'valores_esperados': esperados})
        except Exception:
            pass

    def resizeEvent(self, event):
        super().resizeEvent(event)


__all__ = [
    'MainWindow'
]
