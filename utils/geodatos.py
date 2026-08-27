"""Carga, validación y enriquecimiento del GeoJSON de entidades federativas.

A cada feature se le inyectan las propiedades `clave`, `entidad` e `iso`,
de modo que el resto del proyecto trabaje siempre con la clave INEGI y nunca
dependa de cómo esté escrito el nombre en el archivo original.
"""

import copy
import json
from dataclasses import dataclass, field
from pathlib import Path

import streamlit as st

from config import configuracion as cfg
from config.catalogo import POR_CLAVE, TOTAL_ENTIDADES
from utils.normalizacion import claves_faltantes, resolver_clave


class ErrorGeoJSON(Exception):
    """Problema al leer o validar el archivo GeoJSON."""


@dataclass
class ReporteGeoJSON:
    """Resultado de la validación, para mostrarlo en la interfaz."""
    total_features: int = 0
    propiedad_nombre: str = ""
    reconocidas: int = 0
    sin_reconocer: list[str] = field(default_factory=list)
    faltantes: list[str] = field(default_factory=list)
    duplicadas: list[str] = field(default_factory=list)

    @property
    def es_valido(self) -> bool:
        return (
            self.reconocidas == TOTAL_ENTIDADES
            and not self.sin_reconocer
            and not self.faltantes
            and not self.duplicadas
        )


def _leer_archivo(ruta: Path) -> dict:
    if not ruta.exists():
        raise ErrorGeoJSON(
            f"No se encontró el archivo GeoJSON en:\n{ruta}\n\n"
            "Colócalo en data/geojson/mexico_estados.geojson "
            "(consulta el README para la fuente de descarga)."
        )

    try:
        with ruta.open("r", encoding="utf-8") as archivo:
            contenido = json.load(archivo)
    except json.JSONDecodeError as error:
        raise ErrorGeoJSON(f"El archivo GeoJSON no es un JSON válido: {error}") from error

    if contenido.get("type") != "FeatureCollection":
        raise ErrorGeoJSON("El archivo debe ser un GeoJSON de tipo 'FeatureCollection'.")

    if not contenido.get("features"):
        raise ErrorGeoJSON("El archivo GeoJSON no contiene entidades (features).")

    return contenido


def _detectar_propiedad_nombre(features: list[dict]) -> str:
    """Identifica cuál propiedad del GeoJSON contiene el nombre del estado."""
    propiedades = features[0].get("properties", {})
    for candidata in cfg.PROPIEDADES_NOMBRE:
        if candidata in propiedades:
            return candidata

    raise ErrorGeoJSON(
        "No se encontró la propiedad con el nombre de la entidad. "
        f"Se buscaron: {', '.join(cfg.PROPIEDADES_NOMBRE)}. "
        f"El archivo contiene: {', '.join(propiedades) or '(ninguna)'}. "
        "Agrega el nombre correcto a PROPIEDADES_NOMBRE en config/configuracion.py."
    )


def _enriquecer(geojson: dict, propiedad: str) -> tuple[dict, ReporteGeoJSON]:
    """Agrega clave/entidad/iso a cada feature y arma el reporte de validación."""
    resultado = copy.deepcopy(geojson)
    reporte = ReporteGeoJSON(
        total_features=len(resultado["features"]),
        propiedad_nombre=propiedad,
    )

    vistas: set[str] = set()

    for feature in resultado["features"]:
        propiedades = feature.setdefault("properties", {})
        nombre_original = propiedades.get(propiedad)
        clave = resolver_clave(nombre_original)

        if clave is None:
            reporte.sin_reconocer.append(str(nombre_original))
            propiedades[cfg.PROP_CLAVE] = ""
            propiedades[cfg.PROP_ENTIDAD] = str(nombre_original)
            propiedades[cfg.PROP_ISO] = ""
            continue

        if clave in vistas:
            reporte.duplicadas.append(clave)
        vistas.add(clave)

        entidad = POR_CLAVE[clave]
        propiedades[cfg.PROP_CLAVE] = clave
        propiedades[cfg.PROP_ENTIDAD] = entidad.nombre
        propiedades[cfg.PROP_ISO] = entidad.iso

    reporte.reconocidas = len(vistas)
    reporte.faltantes = [POR_CLAVE[c].nombre for c in claves_faltantes(vistas)]
    return resultado, reporte


@st.cache_data(show_spinner="Cargando geometría de las entidades federativas...")
def cargar_entidades(ruta: str | None = None) -> tuple[dict, ReporteGeoJSON]:
    """Devuelve el GeoJSON enriquecido y su reporte de validación.

    El resultado se cachea: el archivo se lee una sola vez por sesión.
    """
    destino = Path(ruta) if ruta else cfg.RUTA_GEOJSON
    geojson = _leer_archivo(destino)
    propiedad = _detectar_propiedad_nombre(geojson["features"])
    return _enriquecer(geojson, propiedad)


def claves_del_geojson(geojson: dict) -> list[str]:
    """Claves INEGI presentes en el GeoJSON, en orden alfabético de entidad."""
    claves = {
        f["properties"].get(cfg.PROP_CLAVE)
        for f in geojson.get("features", [])
        if f["properties"].get(cfg.PROP_CLAVE)
    }
    return sorted(claves)
