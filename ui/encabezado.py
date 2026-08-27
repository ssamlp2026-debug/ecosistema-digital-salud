"""Encabezado y estilos globales de la aplicación."""

import streamlit as st

from config import configuracion as cfg


def aplicar_estilos() -> None:
    """Carga la hoja de estilos del proyecto, si existe."""
    if cfg.RUTA_ESTILOS.exists():
        css = cfg.RUTA_ESTILOS.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def render_encabezado() -> None:
    st.markdown(
        f"""
        <div class="eds-encabezado">
            <h1>{cfg.ICONO_APP} {cfg.TITULO_APP}</h1>
            <p class="eds-subtitulo">{cfg.SUBTITULO_APP}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(f'<p class="eds-descripcion">{cfg.DESCRIPCION_APP}</p>',
                unsafe_allow_html=True)
