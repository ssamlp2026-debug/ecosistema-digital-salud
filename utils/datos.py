"""Lectura de datos tabulares (CSV / Excel).

Preparado para la siguiente etapa del proyecto: convierte un archivo con
columnas de estado, indicador, valor y categoría en información indexada
por clave INEGI, lista para alimentar el mapa.
"""

from pathlib import Path

import pandas as pd

from utils.normalizacion import resolver_clave

COLUMNA_ESTADO = "Estado"
COLUMNA_INDICADOR = "Indicador"
COLUMNA_VALOR = "Valor"
COLUMNA_CATEGORIA = "Categoría"


class ErrorDatos(Exception):
    """Problema al leer o validar un archivo de datos."""


def cargar_tabla(ruta: str | Path) -> pd.DataFrame:
    """Lee un CSV o un Excel y agrega la columna `clave` con la clave INEGI."""
    destino = Path(ruta)
    if not destino.exists():
        raise ErrorDatos(f"No se encontró el archivo de datos: {destino}")

    if destino.suffix.lower() in (".xlsx", ".xls"):
        tabla = pd.read_excel(destino)
    else:
        tabla = pd.read_csv(destino, encoding="utf-8")

    if COLUMNA_ESTADO not in tabla.columns:
        raise ErrorDatos(
            f"El archivo debe incluir la columna '{COLUMNA_ESTADO}'. "
            f"Columnas encontradas: {', '.join(map(str, tabla.columns))}."
        )

    tabla["clave"] = tabla[COLUMNA_ESTADO].map(resolver_clave)
    return tabla


def estados_no_reconocidos(tabla: pd.DataFrame) -> list[str]:
    """Nombres del archivo que no corresponden a ninguna entidad federativa."""
    sin_clave = tabla[tabla["clave"].isna()]
    return sorted(sin_clave[COLUMNA_ESTADO].astype(str).unique())


def categorias_por_clave(tabla: pd.DataFrame, indicador: str | None = None) -> dict[str, str]:
    """Devuelve {clave INEGI: categoría} para un indicador."""
    filtrada = tabla.dropna(subset=["clave"])
    if indicador is not None:
        filtrada = filtrada[filtrada[COLUMNA_INDICADOR] == indicador]

    return dict(zip(filtrada["clave"], filtrada[COLUMNA_CATEGORIA]))
