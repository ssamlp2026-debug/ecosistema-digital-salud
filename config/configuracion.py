

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DIR_DATOS = BASE_DIR / "data"
DIR_GEOJSON = DIR_DATOS / "geojson"
DIR_EJEMPLO = DIR_DATOS / "ejemplo"
DIR_ASSETS = BASE_DIR / "assets"

RUTA_GEOJSON = DIR_GEOJSON / "mexico_estados.geojson"
RUTA_ESTILOS = DIR_ASSETS / "estilos.css"
RUTA_DATOS_EJEMPLO = DIR_EJEMPLO / "datos_ejemplo.csv"

# Archivo de indicadores de implementación. Se busca en orden: primero en
# data/, que es donde corresponde, y luego en la raíz del proyecto, que es
# donde resulta cómodo tenerlo mientras se captura.
NOMBRE_EXCEL_INDICADORES = "Personasl y establecimientos.xlsx"
RUTAS_EXCEL_INDICADORES = (
    DIR_DATOS / NOMBRE_EXCEL_INDICADORES,
    BASE_DIR / NOMBRE_EXCEL_INDICADORES,
)

# Logo institucional. Se busca en assets/ con cualquiera de estas extensiones,
# así da igual si el archivo se guarda como .png, .svg o .jpg.
NOMBRE_LOGO = "logo_snsp"
EXTENSIONES_LOGO = (".png", ".svg", ".jpg", ".jpeg", ".webp")

# Banda institucional superior: identidad gráfica del Gobierno de México.
# Cada entrada es (nombre del archivo en assets/, texto alternativo).
IMAGEN_BANDA_IZQUIERDA = ("logo_salud", "Secretaría de Salud")
IMAGENES_BANDA_DERECHA = (
    ("imagen_bandera", "Ilustración de una mujer portando la bandera de México"),
    ("logo_gobmx", "Gobierno de México"),
)


def buscar_imagen(nombre: str):
    """Ruta de una imagen de assets/, probando las extensiones admitidas.

    Devuelve None si el archivo todavía no se ha guardado, para que la
    interfaz pueda omitirla en lugar de fallar.
    """
    for extension in EXTENSIONES_LOGO:
        candidato = DIR_ASSETS / f"{nombre}{extension}"
        if candidato.exists():
            return candidato
    return None


def buscar_logo():
    """Ruta del logo institucional del SNSP."""
    return buscar_imagen(NOMBRE_LOGO)

# Propiedades del GeoJSON donde puede venir el nombre de la entidad.
# Se prueban en orden; así el proyecto tolera otros archivos (INEGI, Natural Earth).
PROPIEDADES_NOMBRE = ("name", "NOMBRE", "NOM_ENT", "nom_ent", "ESTADO", "estado", "NOM_AGEE")

# Nombres de las propiedades que el proyecto inyecta en cada feature.
PROP_CLAVE = "clave"
PROP_ENTIDAD = "entidad"
PROP_ISO = "iso"
PROP_ESTABLECIMIENTOS = "establecimientos_atendidos"
PROP_PERSONAL = "personal_asignado"

# Vista inicial del mapa (centro geográfico aproximado de México).
CENTRO_MEXICO = (23.6345, -102.5528)
ZOOM_INICIAL = 5
ZOOM_MINIMO = 4
ZOOM_MAXIMO = 10
LIMITES_MEXICO = ((14.0, -119.0), (33.0, -86.0))  # (suroeste, noreste)
# Mapa base. CARTO dejó de permitir el uso anónimo de sus teselas y las
# devuelve con la marca de agua "API KEY REQUIRED", así que se usa el lienzo
# gris claro de Esri: no requiere llave y tiene un aspecto equivalente.
# Ojo con el orden de los ejes: Esri sirve las teselas como {z}/{y}/{x}.
TILES_BASE = (
    "https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/"
    "World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}"
)
ATRIBUCION_TILES = "Esri, HERE, Garmin, © OpenStreetMap contributors"
ALTURA_MAPA = 560

# Textos de la interfaz.
TITULO_APP = "ECOSISTEMA DIGITAL EN SALUD"
SUBTITULO_APP = (
    "Plataforma para la visualización y análisis de información "

)
DESCRIPCION_APP = (
    "Esta plataforma integra información geográfica de las entidades federativas "
    "como base para la consulta y el análisis de indicadores del sector salud. "
)
ICONO_APP = "🏥"
