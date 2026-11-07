"""Compara rendimiento: búsqueda lineal (legado) vs índice por ISBN (nuevo diseño)."""
import time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from biblioteca.modelos import Libro
from biblioteca.repositorios import RepositorioLibrosMemoria

TAMANOS = [1_000, 5_000, 10_000, 50_000, 100_000]
REPETICIONES = 200
lineal_ms, indexado_ms = [], []

for n in TAMANOS:
    lista = [Libro(str(i), f"Titulo {i}", f"Autor {i}") for i in range(n)]
    repo = RepositorioLibrosMemoria()
    for l in lista:
        repo.agregar(l)
    objetivo = str(n - 1)  # peor caso para la búsqueda lineal

    t = time.perf_counter()
    for _ in range(REPETICIONES):
        next(l for l in lista if l.isbn == objetivo)
    lineal_ms.append((time.perf_counter() - t) / REPETICIONES * 1000)

    t = time.perf_counter()
    for _ in range(REPETICIONES):
        repo.obtener(objetivo)
    indexado_ms.append((time.perf_counter() - t) / REPETICIONES * 1000)

    print(f"n={n:>7}  lineal={lineal_ms[-1]:.4f} ms  indexado={indexado_ms[-1]:.6f} ms")

plt.figure(figsize=(8, 5))
plt.plot(TAMANOS, lineal_ms, "o-", label="Sistema actual (búsqueda lineal)")
plt.plot(TAMANOS, indexado_ms, "s-", label="Sistema propuesto (índice por ISBN)")
plt.xlabel("Cantidad de libros en el catálogo")
plt.ylabel("Tiempo por consulta (ms)")
plt.title("Rendimiento de consulta: antes vs. después")
plt.grid(alpha=.3); plt.legend(); plt.tight_layout()
plt.savefig("docs/grafico_rendimiento.png", dpi=150)
print("Gráfico guardado en docs/grafico_rendimiento.png")
