"""Leyenda de colores del mapa."""

import streamlit as st

from config import colores as paleta


def _chip(color: str, etiqueta: str) -> str:
    return (
        f'<span class="eds-chip">'
        f'<span class="eds-cuadro" style="background:{color}"></span>{etiqueta}'
        f"</span>"
    )


def render_leyenda() -> None:
    """Explica el significado de los colores del mapa."""
    st.markdown("#### Leyenda")
    st.caption(
        "Modo actual: **Gris entidades que no participan, Amarillo entidades en proceso, Blanco entraran en futuro"

    )

    chips = _chip(paleta.COLOR_SIN_INFORMACION, "Entidad sin color asignado")
    st.markdown(f'<div class="eds-leyenda">{chips}</div>', unsafe_allow_html=True)

    with st.expander("Escala de color para indicadores (próxima etapa)"):
        st.caption(
            "Al cargar un archivo de datos, el color de cada entidad se tomará "
            "de la categoría del indicador seleccionado:"
        )
        futuros = "".join(
            _chip(color, etiqueta) for etiqueta, color in paleta.COLORES_CATEGORIA.items()
        )
        st.markdown(f'<div class="eds-leyenda">{futuros}</div>', unsafe_allow_html=True)
