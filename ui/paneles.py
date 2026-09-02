"""Paneles laterales e inferiores de la aplicación."""

import streamlit as st

from config import configuracion as cfg
from utils.coloreo import ReporteColores
from utils.geodatos import ReporteGeoJSON


def render_detalle_entidad(propiedades: dict | None) -> None:
    """Información de la entidad seleccionada en el mapa."""
    st.markdown("#### Entidad seleccionada")

    if not propiedades:
        st.info("Haz clic en un estado del mapa para ver su información.")
        return

    st.markdown(f"**{propiedades.get(cfg.PROP_ENTIDAD, 'Sin identificar')}**")
    st.write(f"Clave INEGI: `{propiedades.get(cfg.PROP_CLAVE, '')}`")
    st.write(f"Código ISO: `{propiedades.get(cfg.PROP_ISO, '')}`")
    st.caption("Los indicadores de esta entidad se mostrarán aquí al integrar "
               "las fuentes de datos.")


def render_panel_indicadores(total_entidades: int) -> None:
    """Área preparada para los indicadores de salud."""
    st.markdown("#### Indicadores")

    columnas = st.columns(4)
    columnas[0].metric("Entidades federativas", total_entidades)
    columnas[1].metric("Indicadores cargados", 0)
    columnas[2].metric("Fuentes de datos", 0)
    columnas[3].metric("Última actualización", "—")

    st.caption("Espacio reservado para las métricas de la plataforma. "
               "Se poblará conforme se integren las bases de datos de salud.")


def render_diagnostico(reporte_geo: ReporteGeoJSON, reporte_color: ReporteColores) -> None:
    """Muestra advertencias solo cuando algo no coincide."""
    if reporte_geo.sin_reconocer:
        st.warning(
            "Entidades del GeoJSON que no se reconocieron: "
            + ", ".join(reporte_geo.sin_reconocer)
            + ". Agrega el nombre como alias en `config/catalogo.py`."
        )

    if reporte_geo.faltantes:
        st.warning(
            "Entidades del catálogo ausentes en el GeoJSON: "
            + ", ".join(reporte_geo.faltantes)
        )

    if reporte_geo.duplicadas:
        st.warning("Hay entidades repetidas en el GeoJSON: "
                   + ", ".join(reporte_geo.duplicadas))

    if reporte_color.sin_reconocer:
        st.warning(
            "Nombres de `COLORES_ESTADOS` que no corresponden a ninguna entidad: "
            + ", ".join(reporte_color.sin_reconocer)
        )

    if reporte_color.sin_color:
        st.info(
            "Entidades sin color definido (se muestran en gris): "
            + ", ".join(reporte_color.sin_color)
        )

    with st.expander("Estado de la validación"):
        st.write(f"Propiedad de nombre detectada en el GeoJSON: "
                 f"`{reporte_geo.propiedad_nombre}`")
        st.write(f"Geometrías leídas: **{reporte_geo.total_features}**")
        st.write(f"Entidades reconocidas: **{reporte_geo.reconocidas} / 32**")
        st.write(f"Colores asignados: **{reporte_color.asignados} / 32**")
