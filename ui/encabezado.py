"""Encabezado de la aplicación."""

import base64

import streamlit as st

from config import configuracion as cfg

_TIPOS_MIME = {
    ".png": "image/png",
    ".svg": "image/svg+xml",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
}


def aplicar_estilos() -> None:
    """Carga la hoja de estilos del proyecto, si existe."""
    if cfg.RUTA_ESTILOS.exists():
        css = cfg.RUTA_ESTILOS.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def logo_como_datauri() -> str | None:
    """Codifica el logo para incrustarlo en el HTML del encabezado."""
    # El logo es decorativo: si no se puede resolver, el encabezado se
    # dibuja solo con el título en lugar de tumbar la página.
    try:
        ruta = cfg.buscar_logo()
    except Exception:
        return None
    if ruta is None:
        return None

    mime = _TIPOS_MIME.get(ruta.suffix.lower(), "image/png")
    datos = base64.b64encode(ruta.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{datos}"


def render_encabezado() -> None:
    logo = logo_como_datauri()
    imagen = (
        f'<img class="eds-logo" src="{logo}" alt="Servicio Nacional de Salud Pública">'
        if logo
        else ""
    )

    st.markdown(
        f"""
        <div class="eds-encabezado">
            {imagen}
            <div class="eds-titulos">
                <h1>{cfg.TITULO_APP}</h1>
                <p class="eds-subtitulo">{cfg.SUBTITULO_APP}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(f'<p class="eds-descripcion">{cfg.DESCRIPCION_APP}</p>',
                unsafe_allow_html=True)
