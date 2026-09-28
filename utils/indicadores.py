"""Lectura de los indicadores de implementación desde el archivo Excel.

Responsabilidad única: convertir el Excel en estructuras listas para mostrar.
La lógica de lectura es independiente de la interfaz; solo la envoltura con
caché conoce Streamlit, igual que en utils/geodatos.py.

Las columnas se reconocen por nombre normalizado y por sinónimos, de modo que
el archivo pueda renombrarse o ampliarse sin tocar el código.
"""

from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd
import streamlit as st

from config import configuracion as cfg
from utils.normalizacion import normalizar_texto, resolver_clave

# Sinónimos aceptados para cada indicador, en texto normalizado.
# Para admitir una variante nueva basta con agregarla a su tupla.
COLUMNAS_INDICADORES: dict[str, tuple[str, ...]] = {
    "personal_asignado": (
        "personal asignado",
        "personal con asignacion",
        "personal con asignacion en la implementacion",
        "personal con asignaciones en la implementacion",
    ),
    "personal_programado": (
        "personal programado",
        "personal con asignacion programado",
        "personal con asignaciones programado",
        "personal con asignaciones programadas",
    ),
    "establecimientos_atendidos": (
        "establecimientos atendidos",
        "establecimientos de salud atendidos",
    ),
    "establecimientos_programados": (
        "establecimientos programados",
        "establecimientos de salud programados",
    ),
}

COLUMNAS_ENTIDAD = (
    "nombre estado",
    "entidad",
    "entidad federativa",
    "nombre de la entidad",
    "estado",
    "nombre entidad",
)
COLUMNAS_CLAVE = ("clave entidad", "clave", "cve ent", "clave inegi")

# Etiqueta visible de cada indicador.
ETIQUETAS: dict[str, str] = {
    "personal_asignado": "Personal con asignación en la implementación",
    "personal_programado": "Personal con asignaciones programado",
    "establecimientos_atendidos": "Establecimientos de salud atendidos",
    "establecimientos_programados": "Establecimientos de salud programados",
}

SIN_DATO = "Sin dato"

# Indicadores que evidencian avance real de una entidad, usados para contar
# cuántas están participando en actividades.
INDICADORES_DE_PARTICIPACION = ("personal_asignado", "establecimientos_atendidos")


class ErrorIndicadores(Exception):
    """El archivo de indicadores no existe o no se pudo interpretar."""


@dataclass
class TablaIndicadores:
    """Indicadores por entidad, más el diagnóstico de la lectura."""

    por_clave: dict[str, dict[str, float | None]] = field(default_factory=dict)
    columnas_encontradas: list[str] = field(default_factory=list)
    columnas_ausentes: list[str] = field(default_factory=list)
    filas_sin_reconocer: list[str] = field(default_factory=list)
    ruta: str = ""

    def de_entidad(self, clave: str) -> dict[str, float | None] | None:
        """Indicadores de una entidad, o None si no aparece en el archivo."""
        return self.por_clave.get(clave)

    def tiene_valores(self) -> bool:
        """True si al menos un indicador tiene un valor capturado."""
        return any(
            valor is not None
            for fila in self.por_clave.values()
            for valor in fila.values()
        )


def ruta_excel() -> Path | None:
    """Primera ubicación donde aparezca el archivo de indicadores."""
    for candidata in cfg.RUTAS_EXCEL_INDICADORES:
        if candidata.exists():
            return candidata
    return None


def _identificar_columnas(columnas) -> tuple[dict[str, str], str | None, str | None]:
    """Relaciona las columnas reales del Excel con los indicadores conocidos."""
    normalizadas = {normalizar_texto(c): c for c in columnas}

    encontradas: dict[str, str] = {}
    for indicador, sinonimos in COLUMNAS_INDICADORES.items():
        for sinonimo in sinonimos:
            if sinonimo in normalizadas:
                encontradas[indicador] = normalizadas[sinonimo]
                break

    columna_entidad = next(
        (normalizadas[n] for n in COLUMNAS_ENTIDAD if n in normalizadas), None
    )
    columna_clave = next(
        (normalizadas[n] for n in COLUMNAS_CLAVE if n in normalizadas), None
    )
    return encontradas, columna_entidad, columna_clave


def _a_numero(valor) -> float | None:
    """Convierte a número; devuelve None si la celda está vacía o no es válida."""
    if valor is None:
        return None
    if isinstance(valor, str):
        valor = valor.strip().replace(",", "")
        if not valor:
            return None
    try:
        if pd.isna(valor):
            return None
    except (TypeError, ValueError):
        pass
    try:
        numero = float(valor)
    except (TypeError, ValueError):
        return None
    return None if pd.isna(numero) else numero


def leer_indicadores(ruta: str | Path | None = None) -> TablaIndicadores:
    """Lee el Excel y devuelve los indicadores indexados por clave INEGI."""
    destino = Path(ruta) if ruta else ruta_excel()
    if destino is None or not destino.exists():
        raise ErrorIndicadores(
            "No se encontró el archivo de indicadores. Se buscó en:\n"
            + "\n".join(str(r) for r in cfg.RUTAS_EXCEL_INDICADORES)
        )

    try:
        hojas = pd.read_excel(destino, sheet_name=None, engine="openpyxl")
    except Exception as error:
        raise ErrorIndicadores(
            f"No se pudo leer el archivo de indicadores: {error}"
        ) from error

    # Se usa la primera hoja que tenga una columna de entidad o de clave.
    for tabla in hojas.values():
        encontradas, col_entidad, col_clave = _identificar_columnas(tabla.columns)
        if col_entidad or col_clave:
            break
    else:
        raise ErrorIndicadores(
            "Ninguna hoja del archivo tiene una columna que identifique a la "
            "entidad federativa. Se esperaba alguna de: "
            + ", ".join(COLUMNAS_ENTIDAD + COLUMNAS_CLAVE)
        )

    reporte = TablaIndicadores(
        columnas_encontradas=sorted(encontradas),
        columnas_ausentes=sorted(set(COLUMNAS_INDICADORES) - set(encontradas)),
        ruta=str(destino),
    )

    for _, fila in tabla.iterrows():
        # La clave INEGI es el identificador más fiable; el nombre es el respaldo.
        clave = None
        if col_clave is not None:
            clave = resolver_clave(fila[col_clave])
        if clave is None and col_entidad is not None:
            clave = resolver_clave(fila[col_entidad])

        if clave is None:
            etiqueta = fila[col_entidad] if col_entidad is not None else fila[col_clave]
            if pd.notna(etiqueta):
                reporte.filas_sin_reconocer.append(str(etiqueta))
            continue

        reporte.por_clave[clave] = {
            indicador: _a_numero(fila[columna])
            for indicador, columna in encontradas.items()
        }

    return reporte


def resumen_general(tabla: TablaIndicadores) -> dict[str, float | None]:
    """Totales nacionales calculados a partir de la tabla por entidad.

    Se calculan aquí en lugar de leerse de una hoja aparte para que el resumen
    no pueda desincronizarse de los datos por entidad.
    """
    totales: dict[str, float | None] = {}

    for indicador in COLUMNAS_INDICADORES:
        valores = [
            fila.get(indicador)
            for fila in tabla.por_clave.values()
            if fila.get(indicador) is not None
        ]
        totales[indicador] = sum(valores) if valores else None

    # "Participando" = la entidad tiene avance real, no solo cifras programadas.
    # Se cuenta si ya hay personal asignado o establecimientos atendidos; tener
    # únicamente valores programados significa estar en la programación, no
    # participando. Para cambiar el criterio basta con editar esta tupla.
    totales["entidades_participando"] = sum(
        1
        for fila in tabla.por_clave.values()
        if any(
            (fila.get(indicador) or 0) > 0
            for indicador in INDICADORES_DE_PARTICIPACION
        )
    )

    return totales


def formatear(valor: float | None) -> str:
    """Número con separador de miles; 'Sin dato' cuando la celda está vacía."""
    if valor is None:
        return SIN_DATO
    if float(valor).is_integer():
        return f"{int(valor):,}"
    return f"{valor:,.2f}"


@st.cache_data(show_spinner="Leyendo indicadores de implementación...")
def _leer_cacheado(ruta: str, marca_tiempo: float, tamano: int) -> TablaIndicadores:
    """Envoltura cacheada. La fecha y el tamaño forman parte de la llave."""
    return leer_indicadores(ruta)


def cargar_indicadores() -> TablaIndicadores:
    """Lee el Excel una sola vez, y lo vuelve a leer en cuanto el archivo cambia.

    Incluir la fecha de modificación y el tamaño en la llave del caché es lo
    que hace que baste con guardar el Excel para que la aplicación muestre los
    datos nuevos, sin reiniciar el servidor.
    """
    destino = ruta_excel()
    if destino is None:
        raise ErrorIndicadores(
            "No se encontró el archivo de indicadores. Se buscó en:\n"
            + "\n".join(str(r) for r in cfg.RUTAS_EXCEL_INDICADORES)
        )

    estado = destino.stat()
    return _leer_cacheado(str(destino), estado.st_mtime, estado.st_size)


def anotar_geojson(geojson: dict, tabla: TablaIndicadores) -> dict:
    """Copia del GeoJSON con los indicadores listos para el globo del mapa."""
    import copy

    resultado = copy.deepcopy(geojson)
    for feature in resultado.get("features", []):
        propiedades = feature.setdefault("properties", {})
        fila = tabla.de_entidad(propiedades.get(cfg.PROP_CLAVE, "")) or {}
        propiedades[cfg.PROP_ESTABLECIMIENTOS] = formatear(
            fila.get("establecimientos_atendidos")
        )
        propiedades[cfg.PROP_PERSONAL] = formatear(fila.get("personal_asignado"))
    return resultado
