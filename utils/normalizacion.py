"""Normalización de nombres de entidades federativas.

Traduce cualquier forma de escribir una entidad ("CDMX", "Distrito Federal",
"Edo. de México", "MX-JAL", "14") a su clave INEGI canónica.
"""

import re
import unicodedata

from config.catalogo import ENTIDADES, POR_CLAVE

# Prefijos que no aportan información y que suelen anteceder al nombre.
_PREFIJOS = (
    "estado libre y soberano de ",
    "estado de ",
    "entidad de ",
    "edo de ",
    "edo ",
)


def normalizar_texto(valor) -> str:
    """Minúsculas, sin acentos, sin puntuación y sin espacios repetidos."""
    texto = unicodedata.normalize("NFKD", str(valor))
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = texto.lower()
    texto = re.sub(r"[^a-z0-9]+", " ", texto)
    return re.sub(r"\s+", " ", texto).strip()


def _sin_prefijo(texto: str) -> str:
    for prefijo in _PREFIJOS:
        if texto.startswith(prefijo):
            return texto[len(prefijo):].strip()
    return texto


def _construir_indice() -> dict[str, str]:
    """Índice {texto normalizado: clave INEGI} con todas las variantes conocidas."""
    indice: dict[str, str] = {}

    def registrar(valor, clave: str) -> None:
        llave = normalizar_texto(valor)
        if not llave:
            return
        anterior = indice.get(llave)
        if anterior is not None and anterior != clave:
            raise ValueError(
                f"Alias ambiguo '{valor}': corresponde a {anterior} y a {clave}. "
                "Revisa config/catalogo.py."
            )
        indice[llave] = clave

    for entidad in ENTIDADES:
        registrar(entidad.nombre, entidad.clave)
        registrar(entidad.nombre_oficial, entidad.clave)
        registrar(entidad.iso, entidad.clave)
        registrar(entidad.clave, entidad.clave)
        registrar(entidad.clave.lstrip("0"), entidad.clave)
        for alias in entidad.alias:
            registrar(alias, entidad.clave)

    return indice


INDICE_ENTIDADES: dict[str, str] = _construir_indice()


def resolver_clave(nombre) -> str | None:
    """Devuelve la clave INEGI de una entidad, o None si no se reconoce."""
    if nombre is None:
        return None

    texto = normalizar_texto(nombre)
    if not texto:
        return None

    clave = INDICE_ENTIDADES.get(texto)
    if clave is not None:
        return clave

    return INDICE_ENTIDADES.get(_sin_prefijo(texto))


def resolver_lote(nombres) -> tuple[dict[str, str], list[str]]:
    """Resuelve varios nombres a la vez.

    Devuelve (mapa {nombre original: clave}, lista de nombres no reconocidos).
    """
    resueltos: dict[str, str] = {}
    desconocidos: list[str] = []

    for nombre in nombres:
        clave = resolver_clave(nombre)
        if clave is None:
            desconocidos.append(str(nombre))
        else:
            resueltos[str(nombre)] = clave

    return resueltos, desconocidos


def claves_faltantes(claves) -> list[str]:
    """Claves INEGI del catálogo que no aparecen en la colección recibida."""
    presentes = set(claves)
    return [clave for clave in POR_CLAVE if clave not in presentes]
