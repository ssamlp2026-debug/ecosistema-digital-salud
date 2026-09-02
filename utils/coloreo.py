"""Decide qué color le corresponde a cada entidad federativa.

Único punto del proyecto donde se resuelve la relación entidad → color.
Hoy la fuente es el diccionario manual de config/colores.py; más adelante
puede ser un DataFrame sin tocar el mapa ni la interfaz.
"""

from dataclasses import dataclass, field

from config import colores as paleta
from config.catalogo import POR_CLAVE
from utils.normalizacion import claves_faltantes, resolver_lote


@dataclass
class ReporteColores:
    """Diagnóstico de la asignación de colores."""
    asignados: int = 0
    sin_reconocer: list[str] = field(default_factory=list)
    sin_color: list[str] = field(default_factory=list)

    @property
    def es_valido(self) -> bool:
        return not self.sin_reconocer and not self.sin_color


def colores_manuales(
    configuracion: dict[str, str] | None = None,
) -> tuple[dict[str, str], ReporteColores]:
    """Convierte {nombre de estado: color} en {clave INEGI: color}."""
    origen = paleta.COLORES_ESTADOS if configuracion is None else configuracion

    resueltos, desconocidos = resolver_lote(origen.keys())
    colores = {clave: origen[nombre] for nombre, clave in resueltos.items()}

    reporte = ReporteColores(
        asignados=len(colores),
        sin_reconocer=desconocidos,
        sin_color=[POR_CLAVE[c].nombre for c in claves_faltantes(colores)],
    )
    return colores, reporte


def colores_por_categoria(
    categorias_por_clave: dict[str, str],
) -> dict[str, str]:
    """Traduce {clave INEGI: categoría} a {clave INEGI: color}.

    Prevista para la etapa de datos: 'Alta' → verde, 'Media' → amarillo,
    'Baja' → rojo, cualquier otro valor → gris.
    """
    return {
        clave: paleta.COLORES_CATEGORIA.get(categoria, paleta.SIN_SNSP)
        for clave, categoria in categorias_por_clave.items()
    }


def color_de(colores: dict[str, str], clave: str) -> str:
    """Color de una entidad, con gris como valor por omisión."""
    return colores.get(clave) or paleta.SIN_SNSP
