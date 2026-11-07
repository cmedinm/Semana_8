# Código LEGADO (monolítico) con malos olores a propósito, para analizar con SonarQube.
import datetime

libros = []
prestamos = []


def hacer_todo(accion, a=None, b=None, c=None, d=None):
    if accion == "agregar":
        libros.append({"isbn": a, "titulo": b, "autor": c, "disp": True})
    elif accion == "buscar":
        r = []
        for l in libros:
            if b.lower() in l["titulo"].lower() or b.lower() in l["autor"].lower():
                r.append(l)
        return r
    elif accion == "prestar":
        for l in libros:
            if l["isbn"] == a:
                if l["disp"] == True:
                    l["disp"] = False
                    prestamos.append({"isbn": a, "rut": b, "f": c})
                    return True
                else:
                    return False
        return False
    elif accion == "devolver":
        for p in prestamos:
            if p["isbn"] == a:
                dias = (d - p["f"]).days
                for l in libros:
                    if l["isbn"] == a:
                        l["disp"] = True
                prestamos.remove(p)
                if dias > 7:
                    return (dias - 7) * 500
                else:
                    return 0
    return None
