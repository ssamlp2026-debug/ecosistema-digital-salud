"""ECOSISTEMA DIGITAL DE SALUD — aplicación principal.

Este archivo solo compone la interfaz. La lógica del mapa, la validación
geográfica y la asignación de colores viven en `utils/`.
"""

import streamlit as st
from streamlit_folium import st_folium

from config import configuracion as cfg
from ui.encabezado import aplicar_estilos, render_encabezado
from ui.leyenda import render_leyenda
from ui.paneles import (
    render_detalle_entidad,
    render_diagnostico,
    render_panel_indicadores,
)
from utils.coloreo import colores_manuales
from utils.geodatos import ErrorGeoJSON, cargar_entidades
from utils.mapa import crear_mapa, entidad_seleccionada


def _icono_pagina():
    """Logo para la pestaña del navegador; emoji como respaldo.

    El icono es decorativo y se resuelve antes de dibujar nada, así que un
    fallo aquí dejaría la aplicación sin abrir. Ante cualquier problema se
    usa el emoji y se continúa.
    """
    try:
        ruta = cfg.buscar_logo()
    except Exception:
        return cfg.ICONO_APP
    return str(ruta) if ruta else cfg.ICONO_APP


def main() -> None:
    st.set_page_config(
        page_title=cfg.TITULO_APP,
        page_icon=_icono_pagina(),
        layout="wide",
    )

    aplicar_estilos()
    render_encabezado()

    try:
        geojson, reporte_geo = cargar_entidades()
    except ErrorGeoJSON as error:
        st.error(str(error))
        st.stop()

    colores, reporte_color = colores_manuales()

    st.divider()

    columna_mapa, columna_lateral = st.columns([3, 1], gap="large")

    with columna_mapa:
        st.markdown("### Mapa de entidades federativas")
        mapa = crear_mapa(geojson, colores)
        resultado = st_folium(
            mapa,
            height=cfg.ALTURA_MAPA,
            use_container_width=True,
            returned_objects=["last_active_drawing"],
        )
        render_leyenda()

    with columna_lateral:
        render_detalle_entidad(entidad_seleccionada(resultado))

    st.divider()
    render_panel_indicadores(reporte_geo.reconocidas)

    st.divider()
    render_diagnostico(reporte_geo, reporte_color)


if __name__ == "__main__":
    main()
