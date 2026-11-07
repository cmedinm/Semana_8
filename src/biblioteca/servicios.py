"""Servicios de negocio (casos de uso)."""
from datetime import date, timedelta
from typing import Dict, List
from .modelos import Libro, Prestamo
from .multas import PoliticaMulta
from .repositorios import RepositorioLibros

DIAS_PRESTAMO = 7


class LibroNoDisponibleError(Exception):
    pass


class ServicioCatalogo:
    def __init__(self, repo: RepositorioLibros) -> None:
        self._repo = repo

    def registrar(self, libro: Libro) -> None:
        self._repo.agregar(libro)

    def buscar(self, texto: str) -> List[Libro]:
        return self._repo.buscar(texto)


class ServicioPrestamos:
    def __init__(self, repo: RepositorioLibros, politica: PoliticaMulta) -> None:
        self._repo = repo
        self._politica = politica
        self._prestamos: Dict[str, Prestamo] = {}

    def prestar(self, isbn: str, rut: str, hoy: date) -> Prestamo:
        libro = self._repo.obtener(isbn)
        if libro is None:
            raise KeyError(f"Libro {isbn} no existe")
        if not libro.disponible:
            raise LibroNoDisponibleError(f"Libro {isbn} no disponible")
        libro.disponible = False
        p = Prestamo(isbn, rut, hoy, hoy + timedelta(days=DIAS_PRESTAMO))
        self._prestamos[isbn] = p
        return p

    def devolver(self, isbn: str, hoy: date) -> int:
        """Devuelve el libro y retorna la multa a pagar (0 si no hay atraso)."""
        p = self._prestamos.pop(isbn, None)
        if p is None:
            raise KeyError(f"No hay préstamo activo para {isbn}")
        p.fecha_devolucion = hoy
        self._repo.obtener(isbn).disponible = True
        return self._politica.calcular(p.fecha_limite, hoy)
