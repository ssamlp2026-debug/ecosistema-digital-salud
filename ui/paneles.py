"""Paneles laterales e inferiores de la aplicación."""

import streamlit as st

from config import configuracion as cfg
from utils import indicadores as ind
from utils.coloreo import ReporteColores
from utils.geodatos import ReporteGeoJSON


def render_detalle_entidad(
    propiedades: dict | None, tabla: ind.TablaIndicadores | None = None
) -> None:
    """Indicadores de la entidad seleccionada en el mapa."""
    st.markdown("#### Entidad seleccionada")

    if not propiedades:
        st.info("Haz clic en un estado del mapa para ver su información.")
        return

    nombre = propiedades.get(cfg.PROP_ENTIDAD, "Sin identificar")
    st.markdown(f"**{nombre}**")

    fila = tabla.de_entidad(propiedades.get(cfg.PROP_CLAVE, "")) if tabla else None
    if fila is None:
        st.warning("No hay información disponible para esta entidad.")
        return

    st.markdown(
        f"🏥 **Establecimientos de salud atendidos:** "
        f"{ind.formatear(fila.get('establecimientos_atendidos'))}"
    )
    st.markdown(
        f"👥 **Personal con asignación en la implementación:** "
        f"{ind.formatear(fila.get('personal_asignado'))}"
    )


def render_resumen_general(tabla: ind.TablaIndicadores) -> None:
    """Resumen nacional de la implementación, calculado desde el Excel."""
    st.markdown("#### Resumen general")

    totales = ind.resumen_general(tabla)

    fila_uno = st.columns(3)
    fila_uno[0].metric(
        "Entidades participando en actividades",
        f"{totales['entidades_participando']} de {len(tabla.por_clave)}",
    )
    fila_uno[1].metric(
        ind.ETIQUETAS["personal_asignado"],
        ind.formatear(totales["personal_asignado"]),
    )
    fila_uno[2].metric(
        ind.ETIQUETAS["personal_programado"],
        ind.formatear(totales["personal_programado"]),
    )

    fila_dos = st.columns(3)
    fila_dos[0].metric(
        ind.ETIQUETAS["establecimientos_atendidos"],
        ind.formatear(totales["establecimientos_atendidos"]),
    )
    fila_dos[1].metric(
        ind.ETIQUETAS["establecimientos_programados"],
        ind.formatear(totales["establecimientos_programados"]),
    )

    if not tabla.tiene_valores():
        st.caption(
            "El archivo de indicadores todavía no tiene valores capturados. "
            "En cuanto los escribas y guardes el Excel, estas cifras se "
            "actualizarán solas."
        )


def render_diagnostico(
    reporte_geo: ReporteGeoJSON,
    reporte_color: ReporteColores,
    tabla: ind.TablaIndicadores | None = None,
) -> None:
    """Muestra advertencias solo cuando algo no coincide."""
    if tabla is not None and tabla.columnas_ausentes:
        faltantes = ", ".join(ind.ETIQUETAS[c] for c in tabla.columnas_ausentes)
        st.info(
            f"El archivo de indicadores todavía no tiene columna para: {faltantes}. "
            "Ese indicador aparece como «Sin dato»; se llenará solo en cuanto "
            "agregues la columna al Excel."
        )

    if tabla is not None and tabla.filas_sin_reconocer:
        st.warning(
            "Filas del Excel que no corresponden a ninguna entidad: "
            + ", ".join(tabla.filas_sin_reconocer)
        )

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

        if tabla is not None:
            st.write(f"Archivo de indicadores: `{tabla.ruta}`")
            st.write(f"Entidades leídas del Excel: **{len(tabla.por_clave)} / 32**")
            st.write(
                "Columnas reconocidas: "
                + (", ".join(ind.ETIQUETAS[c] for c in tabla.columnas_encontradas)
                   or "ninguna")
            )
