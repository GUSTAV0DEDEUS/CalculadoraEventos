# Calculadora de Eventos

Aplicativo desktop para calcular a distribuição de custos de eventos com visualização gráfica.

## 📊 Funcionalidades

- Interface gráfica moderna e intuitiva
- Cálculo automático da distribuição de custos:
  - **Staff**: 12%
  - **Locação**: 9%
  - **CMV**: 30%
  - **Nota**: 12%
  - **Outros (Mockup)**: 37% _(categoria temporária para custos não definidos)_
- Visualização em gráfico de pizza
- Exibição detalhada dos valores calculados

## 🚀 Como Usar

### Executável Windows (Recomendado)

1. Baixe o arquivo `CalculadoraEventos.exe` da pasta `dist`
2. Execute o arquivo (não precisa instalar nada)
3. Digite o valor total do evento
4. Clique em "Calcular"
5. Veja a distribuição dos valores e o gráfico

### Executar o Código Python

#### Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

#### Instalação

1. Clone ou baixe este repositório

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o aplicativo:
```bash
python main.py
```

## 🔨 Gerar o Instalador para Windows

Se você quiser gerar o executável você mesmo:

1. Certifique-se de ter todas as dependências instaladas:
```bash
pip install -r requirements.txt
```

2. Execute o script de build:
```bash
python build.py
```

3. O executável será criado em `dist/CalculadoraEventos.exe`

### Notas sobre o Build

- O processo pode levar alguns minutos
- O executável funciona em qualquer Windows (7, 8, 10, 11)
- Não é necessário ter Python instalado no computador de destino
- O arquivo .exe contém tudo que é necessário para rodar o aplicativo

## 📦 Dependências

- **PySide6**: Framework para interface gráfica (Qt for Python)
- **matplotlib**: Biblioteca para gráficos
- **PyInstaller**: Ferramenta para criar executáveis

## 🎨 Estrutura do Projeto

```
calculadora/
│
├── main.py                 # Ponto de entrada da aplicação
├── build.py               # Script para gerar o executável
├── criar_logo.py          # Script para gerar logo (opcional)
├── requirements.txt       # Lista de dependências
├── README.md             # Este arquivo
│
├── src/                   # Código fonte modular
│   ├── __init__.py
│   ├── main_window.py    # Janela principal
│   │
│   ├── components/       # Componentes da UI
│   │   ├── __init__.py
│   │   ├── header.py              # Componente de cabeçalho
│   │   ├── input_section.py       # Componente de entrada
│   │   ├── results_section.py     # Componente de resultados
│   │   └── chart_section.py       # Componente de gráfico
│   │
│   ├── utils/            # Utilitários e helpers
│   │   ├── __init__.py
│   │   ├── constants.py           # Constantes e estilos
│   │   └── calculator.py          # Lógica de cálculo
│   │
│   └── assets/           # Recursos (logo, imagens)
│       └── logo.png
│
├── dist/                 # Executável (gerado após build)
│   └── CalculadoraEventos.exe
│
└── build/                # Arquivos temporários do build
```

## 💡 Personalização

### Alterar Percentuais

Para modificar os percentuais das categorias, edite o dicionário `PERCENTUAIS` no arquivo `src/utils/constants.py`:

```python
PERCENTUAIS = {
    'Staff': 12.0,
    'Locação': 9.0,
    'CMV': 30.0,
    'Nota': 12.0,
    'Outros (Mockup)': 37.0
}
```

### Adicionar Novas Categorias

1. Adicione a categoria no dicionário `PERCENTUAIS` em `src/utils/constants.py`
2. Certifique-se de que a soma dos percentuais seja 100%
3. Opcionalmente, adicione uma cor correspondente em `CORES`

### Alterar Cores do Gráfico

Modifique a lista `CORES` em `src/utils/constants.py`:

```python
CORES = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
```

### Alterar Estilos

Os estilos CSS estão centralizados em `src/utils/constants.py` no dicionário `ESTILOS`. Você pode personalizar cores, bordas, sombras, etc.

## 🐛 Problemas Comuns

### Erro ao executar o .exe

- **Antivírus bloqueando**: Alguns antivírus podem bloquear executáveis gerados pelo PyInstaller. Adicione uma exceção.
- **Arquivo corrompido**: Baixe novamente ou gere um novo executável.

### Erro "module not found" ao rodar main.py

- Certifique-se de ter instalado as dependências: `pip install -r requirements.txt`

### Build falha

- Verifique se todas as dependências estão instaladas corretamente
- Use Python 3.8 ou superior
- Em Linux/Mac, pode precisar de permissões especiais

## 📝 Licença

Este projeto é de código aberto. Sinta-se livre para usar, modificar e distribuir.

## 👨‍💻 Desenvolvimento

Desenvolvido com Python, PySide6 e matplotlib.

---

**Versão**: 1.0.0  
**Data**: Novembro 2025
