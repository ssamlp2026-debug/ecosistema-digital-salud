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
    """Explica qué significa el color de cada entidad."""
    st.markdown("#### Leyenda")

    chips = "".join(
        _chip(color, etiqueta)
        for etiqueta, color in paleta.COLORES_CATEGORIA.items()
    )
    st.markdown(f'<div class="eds-leyenda">{chips}</div>', unsafe_allow_html=True)
