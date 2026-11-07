from datetime import date
import pytest
from biblioteca.modelos import Libro
from biblioteca.multas import MultaPorDia
from biblioteca.repositorios import RepositorioLibrosMemoria
from biblioteca.servicios import (LibroNoDisponibleError, ServicioCatalogo,
                                  ServicioPrestamos)


@pytest.fixture
def repo():
    r = RepositorioLibrosMemoria()
    r.agregar(Libro("111", "Clean Code", "Robert Martin"))
    r.agregar(Libro("222", "Refactoring", "Martin Fowler"))
    return r


@pytest.fixture
def prestamos(repo):
    return ServicioPrestamos(repo, MultaPorDia(500))


def test_buscar_por_titulo(repo):
    assert [l.isbn for l in ServicioCatalogo(repo).buscar("clean")] == ["111"]


def test_buscar_por_autor(repo):
    assert len(ServicioCatalogo(repo).buscar("martin")) == 2


def test_registrar_libro(repo):
    ServicioCatalogo(repo).registrar(Libro("333", "SOLID", "Autor"))
    assert repo.obtener("333") is not None


def test_prestar_marca_no_disponible(prestamos, repo):
    prestamos.prestar("111", "1-9", date(2026, 11, 1))
    assert repo.obtener("111").disponible is False


def test_prestar_libro_ya_prestado_falla(prestamos):
    prestamos.prestar("111", "1-9", date(2026, 11, 1))
    with pytest.raises(LibroNoDisponibleError):
        prestamos.prestar("111", "2-7", date(2026, 11, 2))


def test_prestar_libro_inexistente(prestamos):
    with pytest.raises(KeyError):
        prestamos.prestar("999", "1-9", date(2026, 11, 1))


def test_devolucion_a_tiempo_sin_multa(prestamos, repo):
    prestamos.prestar("111", "1-9", date(2026, 11, 1))
    assert prestamos.devolver("111", date(2026, 11, 8)) == 0
    assert repo.obtener("111").disponible is True


def test_devolucion_atrasada_con_multa(prestamos):
    prestamos.prestar("111", "1-9", date(2026, 11, 1))
    assert prestamos.devolver("111", date(2026, 11, 11)) == 1500  # 3 días x 500


def test_devolver_sin_prestamo(prestamos):
    with pytest.raises(KeyError):
        prestamos.devolver("111", date(2026, 11, 1))



def test_multa_respeta_tope():
    politica = MultaPorDia(500, tope=2000)
    assert politica.calcular(date(2026, 11, 8), date(2026, 11, 28)) == 2000