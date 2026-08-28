

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DIR_DATOS = BASE_DIR / "data"
DIR_GEOJSON = DIR_DATOS / "geojson"
DIR_EJEMPLO = DIR_DATOS / "ejemplo"
DIR_ASSETS = BASE_DIR / "assets"

RUTA_GEOJSON = DIR_GEOJSON / "mexico_estados.geojson"
RUTA_ESTILOS = DIR_ASSETS / "estilos.css"
RUTA_DATOS_EJEMPLO = DIR_EJEMPLO / "datos_ejemplo.csv"

# Propiedades del GeoJSON donde puede venir el nombre de la entidad.
# Se prueban en orden; así el proyecto tolera otros archivos (INEGI, Natural Earth).
PROPIEDADES_NOMBRE = ("name", "NOMBRE", "NOM_ENT", "nom_ent", "ESTADO", "estado", "NOM_AGEE")

# Nombres de las propiedades que el proyecto inyecta en cada feature.
PROP_CLAVE = "clave"
PROP_ENTIDAD = "entidad"
PROP_ISO = "iso"

# Vista inicial del mapa (centro geográfico aproximado de México).
CENTRO_MEXICO = (23.6345, -102.5528)
ZOOM_INICIAL = 5
ZOOM_MINIMO = 4
ZOOM_MAXIMO = 10
LIMITES_MEXICO = ((14.0, -119.0), (33.0, -86.0))  # (suroeste, noreste)
TILES_BASE = "cartodbpositron"
ALTURA_MAPA = 560

# Textos de la interfaz.
TITULO_APP = "ECOSISTEMA DIGITAL DE SALUD"
SUBTITULO_APP = (
    "Plataforma para la visualización y análisis de información "

)
DESCRIPCION_APP = (
    "Esta plataforma integra información geográfica de las entidades federativas "
    "como base para la consulta y el análisis de indicadores del sector salud. "
)
ICONO_APP = "🏥"
