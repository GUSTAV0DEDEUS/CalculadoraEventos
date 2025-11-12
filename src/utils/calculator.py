from typing import Dict


class CalculadoraCustos:
    def __init__(self, percentuais: Dict[str, float]):
        self.percentuais = percentuais
        self._validar_percentuais()
    
    def _validar_percentuais(self):
        total = sum(self.percentuais.values())
        if abs(total - 100) > 0.01:
            raise ValueError(f"A soma dos percentuais deve ser 100%, não {total}%")
    
    def calcular(self, valor_total: float) -> Dict[str, float]:
        if valor_total < 0:
            raise ValueError("O valor total não pode ser negativo")
        
        valores = {}
        for categoria, percentual in self.percentuais.items():
            valores[categoria] = valor_total * (percentual / 100)
        
        return valores
    
    def formatar_moeda(self, valor: float) -> str:
        return f"R$ {valor:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
    
    def obter_percentual(self, categoria: str) -> float:
        return self.percentuais.get(categoria, 0)
