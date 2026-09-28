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


def imagen_como_datauri(nombre: str) -> str | None:
    """Codifica una imagen de assets/ para incrustarla en el HTML.

    Las imágenes del encabezado son decorativas: si alguna no se puede
    resolver se omite, en lugar de tumbar la página.
    """
    try:
        ruta = cfg.buscar_imagen(nombre)
    except Exception:
        return None
    if ruta is None:
        return None

    mime = _TIPOS_MIME.get(ruta.suffix.lower(), "image/png")
    datos = base64.b64encode(ruta.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{datos}"


def logo_como_datauri() -> str | None:
    """Logo del SNSP listo para incrustar."""
    return imagen_como_datauri(cfg.NOMBRE_LOGO)


def _etiqueta_img(nombre: str, alt: str, clase: str) -> str:
    """Etiqueta <img> con la imagen incrustada, o cadena vacía si no existe."""
    uri = imagen_como_datauri(nombre)
    return f'<img class="{clase}" src="{uri}" alt="{alt}">' if uri else ""


def render_banda_institucional() -> None:
    """Banda superior con la identidad gráfica institucional."""
    izquierda = _etiqueta_img(*cfg.IMAGEN_BANDA_IZQUIERDA, clase="eds-banda-logo")
    derecha = "".join(
        _etiqueta_img(nombre, alt, clase="eds-banda-logo")
        for nombre, alt in cfg.IMAGENES_BANDA_DERECHA
    )

    if not izquierda and not derecha:
        return

    st.markdown(
        f"""
        <div class="eds-banda">
            <div class="eds-banda-grupo">{izquierda}</div>
            <div class="eds-banda-grupo">{derecha}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_encabezado() -> None:
    render_banda_institucional()

    logo = logo_como_datauri()
    # El logo va sobre una tarjeta blanca: su arte es guinda sobre blanco
    # y sin ella se perdería contra el fondo vino del encabezado.
    imagen = (
        '<span class="eds-logo-marco">'
        f'<img class="eds-logo" src="{logo}" alt="Servicio Nacional de Salud Pública">'
        "</span>"
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
