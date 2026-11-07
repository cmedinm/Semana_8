"""Genera el diagrama de arquitectura de microservicios."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(11, 6.5))
ax.set_xlim(0, 11); ax.set_ylim(0, 7); ax.axis("off")

def caja(x, y, w, h, texto, color):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                                fc=color, ec="black", lw=1.2))
    ax.text(x + w/2, y + h/2, texto, ha="center", va="center", fontsize=9, weight="bold")

def flecha(x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", lw=1.4))

caja(4, 6, 3, .8, "Usuarios (Web / Móvil)", "#dddddd")
caja(4, 4.7, 3, .8, "API Gateway\n(autenticación, balanceo)", "#ffd966")
caja(0.3, 2.9, 2.3, 1, "Servicio\nCatálogo\n(búsqueda)", "#9fc5e8")
caja(3.0, 2.9, 2.3, 1, "Servicio\nPréstamos\n(reservas)", "#9fc5e8")
caja(5.7, 2.9, 2.3, 1, "Servicio\nMultas /\nDevoluciones", "#9fc5e8")
caja(8.4, 2.9, 2.3, 1, "Servicio\nUsuarios", "#9fc5e8")
caja(0.3, 1.1, 2.3, .9, "BD Catálogo\n+ caché", "#b6d7a8")
caja(3.0, 1.1, 2.3, .9, "BD Préstamos", "#b6d7a8")
caja(5.7, 1.1, 2.3, .9, "BD Multas", "#b6d7a8")
caja(8.4, 1.1, 2.3, .9, "BD Usuarios", "#b6d7a8")
caja(0.3, 0.05, 10.4, .6, "Docker / Docker Compose (cada servicio en su contenedor, escalable de forma independiente)", "#ead1dc")

flecha(5.5, 6, 5.5, 5.5)
for cx in (1.45, 4.15, 6.85, 9.55):
    flecha(5.5, 4.7, cx, 3.9)
    flecha(cx, 2.9, cx, 2.0)
ax.set_title("Arquitectura propuesta: microservicios en contenedores", fontsize=12, weight="bold")
plt.tight_layout()
plt.savefig("docs/arquitectura.png", dpi=150)
print("Diagrama guardado en docs/arquitectura.png")
