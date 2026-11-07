"""Repositorios. DIP: los servicios dependen de la abstracción, no de la BD."""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from .modelos import Libro


class RepositorioLibros(ABC):
    @abstractmethod
    def agregar(self, libro: Libro) -> None: ...

    @abstractmethod
    def obtener(self, isbn: str) -> Optional[Libro]: ...

    @abstractmethod
    def buscar(self, texto: str) -> List[Libro]: ...


class RepositorioLibrosMemoria(RepositorioLibros):
    """Implementación en memoria con índice por ISBN (búsqueda O(1))."""

    def __init__(self) -> None:
        self._libros: Dict[str, Libro] = {}

    def agregar(self, libro: Libro) -> None:
        self._libros[libro.isbn] = libro

    def obtener(self, isbn: str) -> Optional[Libro]:
        return self._libros.get(isbn)

    def buscar(self, texto: str) -> List[Libro]:
        t = texto.lower()
        return [l for l in self._libros.values()
                if t in l.titulo.lower() or t in l.autor.lower()]
