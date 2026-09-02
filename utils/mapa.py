"""Construcción del mapa interactivo de las entidades federativas.

Este módulo no sabe nada de Streamlit: recibe el GeoJSON ya enriquecido y un
diccionario {clave INEGI: color}, y devuelve un objeto folium.Map.
"""

import folium

from config import colores as paleta
from config import configuracion as cfg


def _funcion_estilo(colores: dict[str, str]):
    """Crea la función que Folium aplica a cada polígono."""

    def estilo(feature):
        clave = feature["properties"].get(cfg.PROP_CLAVE, "")
        return {
            "fillColor": colores.get(clave) or paleta.SIN_SNSP,
            "color": paleta.COLOR_BORDE,
            "weight": paleta.GROSOR_BORDE,
            "fillOpacity": paleta.OPACIDAD_RELLENO,
        }

    return estilo


def _estilo_resaltado(_feature):
    """Estilo al pasar el cursor sobre una entidad."""
    return {
        "color": paleta.COLOR_RESALTADO,
        "weight": paleta.GROSOR_RESALTADO,
        "fillOpacity": 0.95,
    }


def crear_mapa(
    geojson: dict,
    colores: dict[str, str],
    centro: tuple[float, float] = cfg.CENTRO_MEXICO,
    zoom: int = cfg.ZOOM_INICIAL,
) -> folium.Map:
    """Devuelve el mapa de México con las 32 entidades coloreadas."""
    mapa = folium.Map(
        location=centro,
        zoom_start=zoom,
        min_zoom=cfg.ZOOM_MINIMO,
        max_zoom=cfg.ZOOM_MAXIMO,
        tiles=cfg.TILES_BASE,
        control_scale=True,
        zoom_control=True,
        scrollWheelZoom=True,
        dragging=True,
    )

    folium.GeoJson(
        geojson,
        name="Entidades federativas",
        style_function=_funcion_estilo(colores),
        highlight_function=_estilo_resaltado,
        smooth_factor=0.5,
        tooltip=folium.GeoJsonTooltip(
            fields=[cfg.PROP_ENTIDAD],
            aliases=["Entidad:"],
            sticky=True,
            style=(
                "background-color: #FFFFFF; border: 1px solid #1F4E5F; "
                "border-radius: 4px; padding: 6px; font-size: 13px;"
            ),
        ),
        popup=folium.GeoJsonPopup(
            fields=[cfg.PROP_ENTIDAD, cfg.PROP_CLAVE, cfg.PROP_ISO],
            aliases=["Entidad", "Clave INEGI", "Código ISO"],
            localize=True,
            labels=True,
            max_width=320,
        ),
    ).add_to(mapa)

    mapa.fit_bounds(cfg.LIMITES_MEXICO)
    return mapa


def entidad_seleccionada(resultado: dict | None) -> dict | None:
    """Extrae las propiedades de la entidad clicada devuelta por st_folium."""
    if not resultado:
        return None

    dibujo = resultado.get("last_active_drawing")
    if not dibujo:
        return None

    propiedades = dibujo.get("properties") or {}
    return propiedades if propiedades.get(cfg.PROP_CLAVE) else None
