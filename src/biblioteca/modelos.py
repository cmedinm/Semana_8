"""Modelos de dominio (SRP: solo representan datos)."""
from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Libro:
    isbn: str
    titulo: str
    autor: str
    disponible: bool = True


@dataclass
class Usuario:
    rut: str
    nombre: str


@dataclass
class Prestamo:
    isbn: str
    rut: str
    fecha_prestamo: date
    fecha_limite: date
    fecha_devolucion: Optional[date] = None
