"""Catálogo oficial de las 32 entidades federativas de México.

La llave canónica es la clave INEGI de dos
dígitos ("01"-"32"), que es la que utilizan INEGI, la Secretaría de Salud
(DGIS) y CONAPO en sus bases de datos.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Entidad:
    clave: str          # Clave INEGI ("01"-"32")
    iso: str            # Código ISO 3166-2 ("MX-AGU")
    nombre: str         # Nombre de uso común
    nombre_oficial: str # Nombre oficial completo
    alias: tuple = field(default=())


ENTIDADES: tuple[Entidad, ...] = (
    Entidad("01", "MX-AGU", "Aguascalientes", "Aguascalientes", ("AGS",)),
    Entidad("02", "MX-BCN", "Baja California", "Baja California",
            ("BC", "BCN", "Baja California Norte")),
    Entidad("03", "MX-BCS", "Baja California Sur", "Baja California Sur", ("BCS",)),
    Entidad("04", "MX-CAM", "Campeche", "Campeche", ("CAMP",)),
    Entidad("05", "MX-COA", "Coahuila", "Coahuila de Zaragoza", ("COAH",)),
    Entidad("06", "MX-COL", "Colima", "Colima", ("COL",)),
    Entidad("07", "MX-CHP", "Chiapas", "Chiapas", ("CHIS",)),
    Entidad("08", "MX-CHH", "Chihuahua", "Chihuahua", ("CHIH",)),
    Entidad("09", "MX-CMX", "Ciudad de México", "Ciudad de México",
            ("CDMX", "DF", "D.F.", "Distrito Federal", "Cd. de México", "Cd de Mexico")),
    Entidad("10", "MX-DUR", "Durango", "Durango", ("DGO",)),
    Entidad("11", "MX-GUA", "Guanajuato", "Guanajuato", ("GTO",)),
    Entidad("12", "MX-GRO", "Guerrero", "Guerrero", ("GRO",)),
    Entidad("13", "MX-HID", "Hidalgo", "Hidalgo", ("HGO",)),
    Entidad("14", "MX-JAL", "Jalisco", "Jalisco", ("JAL",)),
    Entidad("15", "MX-MEX", "México", "México",
            ("Estado de México", "Edo. de México", "Edo de Mexico", "Edomex",
             "Edo. Méx.", "MEX")),
    Entidad("16", "MX-MIC", "Michoacán", "Michoacán de Ocampo", ("MICH",)),
    Entidad("17", "MX-MOR", "Morelos", "Morelos", ("MOR",)),
    Entidad("18", "MX-NAY", "Nayarit", "Nayarit", ("NAY",)),
    Entidad("19", "MX-NLE", "Nuevo León", "Nuevo León", ("NL", "N.L.")),
    Entidad("20", "MX-OAX", "Oaxaca", "Oaxaca", ("OAX",)),
    Entidad("21", "MX-PUE", "Puebla", "Puebla", ("PUE",)),
    Entidad("22", "MX-QUE", "Querétaro", "Querétaro", ("QRO", "Queretaro de Arteaga")),
    Entidad("23", "MX-ROO", "Quintana Roo", "Quintana Roo", ("QROO", "Q. Roo")),
    Entidad("24", "MX-SLP", "San Luis Potosí", "San Luis Potosí", ("SLP",)),
    Entidad("25", "MX-SIN", "Sinaloa", "Sinaloa", ("SIN",)),
    Entidad("26", "MX-SON", "Sonora", "Sonora", ("SON",)),
    Entidad("27", "MX-TAB", "Tabasco", "Tabasco", ("TAB",)),
    Entidad("28", "MX-TAM", "Tamaulipas", "Tamaulipas", ("TAMPS",)),
    Entidad("29", "MX-TLA", "Tlaxcala", "Tlaxcala", ("TLAX",)),
    Entidad("30", "MX-VER", "Veracruz", "Veracruz de Ignacio de la Llave",
            ("VER", "Veracruz Llave")),
    Entidad("31", "MX-YUC", "Yucatán", "Yucatán", ("YUC",)),
    Entidad("32", "MX-ZAC", "Zacatecas", "Zacatecas", ("ZAC",)),
)

POR_CLAVE: dict[str, Entidad] = {e.clave: e for e in ENTIDADES}

TOTAL_ENTIDADES = 32


def nombre_de(clave: str) -> str:
    """Nombre de uso común de una entidad a partir de su clave INEGI."""
    entidad = POR_CLAVE.get(clave)
    return entidad.nombre if entidad else "Sin identificar"
