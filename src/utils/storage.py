"""
Storage simples em JSON para guardar clientes e seus dados
"""
import json
import os
from typing import Dict, Any

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
CLIENTS_FILE = os.path.join(DATA_DIR, 'clients.json')


DEFAULT_CLIENT = {
    'name': 'Novo Cliente',
    'percentuais': {
        'Staff': 12.0,
        'Locação': 9.0,
        'CMV': 30.0,
        'Nota': 12.0,
        'Lucro': 37.0
    },
    'valor_total': 0.0,
    'valores_reais': {
        'Staff': 0.0,
        'Locação': 0.0,
        'CMV': 0.0,
        'Nota': 0.0,
        'Lucro': 0.0
    },
    'historico': []
}


def _ensure_storage():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(CLIENTS_FILE):
        with open(CLIENTS_FILE, 'w', encoding='utf-8') as f:
            json.dump({'clients': []}, f, indent=2, ensure_ascii=False)


def load_all_clients() -> Dict[str, Any]:
    _ensure_storage()
    with open(CLIENTS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_all_clients(data: Dict[str, Any]):
    _ensure_storage()
    with open(CLIENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def create_client(name: str = None) -> Dict[str, Any]:
    data = load_all_clients()
    client = DEFAULT_CLIENT.copy()
    # Deep copy percentuais and valores_reais
    client['percentuais'] = DEFAULT_CLIENT['percentuais'].copy()
    client['valores_reais'] = DEFAULT_CLIENT['valores_reais'].copy()
    client['name'] = name or DEFAULT_CLIENT['name']
    data['clients'].append(client)
    save_all_clients(data)
    return client


def update_client(index: int, client_data: Dict[str, Any]):
    data = load_all_clients()
    if index < 0 or index >= len(data['clients']):
        raise IndexError('Client index out of range')
    data['clients'][index] = client_data
    save_all_clients(data)


def get_client(index: int) -> Dict[str, Any]:
    data = load_all_clients()
    if index < 0 or index >= len(data['clients']):
        raise IndexError('Client index out of range')
    return data['clients'][index]
