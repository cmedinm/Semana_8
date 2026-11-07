"""Políticas de multa. OCP: se agregan nuevas políticas sin modificar el servicio."""
from abc import ABC, abstractmethod
from datetime import date
from typing import Optional


class PoliticaMulta(ABC):
    @abstractmethod
    def calcular(self, fecha_limite: date, fecha_devolucion: date) -> int: ...


class MultaPorDia(PoliticaMulta):
    def __init__(self, valor_dia: int = 500, tope: Optional[int] = None) -> None:
        self.valor_dia = valor_dia
        self.tope = tope

    def calcular(self, fecha_limite: date, fecha_devolucion: date) -> int:
        dias_atraso = (fecha_devolucion - fecha_limite).days
        multa = max(0, dias_atraso) * self.valor_dia
        if self.tope is not None:
            return min(multa, self.tope)
        return multa
