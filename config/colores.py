
# Color a cada entidad federativa.
COLORES_ESTADOS: dict[str, str] = {
    "Aguascalientes": "#D3D3D3",
    "Baja California": "#fafafa",
    "Baja California Sur": "#fafafa",
    "Campeche": "#fafafa",
    "Chiapas": "#de70e6",
    "Chihuahua": "#D3D3D3",
    "Ciudad de México": "#fafafa",
    "Coahuila": "#D3D3D3",
    "Colima": "#f7e62b",
    "Durango": "#D3D3D3",
    "Estado de México": "#f7e62b",
    "Guanajuato": "#D3D3D3",
    "Guerrero": "#f7e62b",
    "Hidalgo": "#f7e62b",
    "Jalisco": "#D3D3D3",
    "Michoacán": "#fafafa",
    "Morelos": "#f7e62b",
    "Nayarit": "#fafafa",
    "Nuevo León": "#D3D3D3",
    "Oaxaca": "#f7e62b",
    "Puebla": "#f7e62b",
    "Querétaro": "#D3D3D3",
    "Quintana Roo": "#fafafa",
    "San Luis Potosí": "#fafafa",
    "Sinaloa": "#fafafa",
    "Sonora": "#f7e62b",
    "Tabasco": "#fafafa",
    "Tamaulipas": "#f7e62b",
    "Tlaxcala": "#fafafa",
    "Veracruz": "#f7e62b",
    "Yucatán": "#fafafa",
    "Zacatecas": "#fafafa",
}

# Color para cualquier entidad sin color o sin dato asignado.
SIN_SNSP = "#de70e6"

# Paleta semántica que se usará cuando el mapa se alimente de datos.
COLORES_CATEGORIA: dict[str, str] = {
    "Próximos por entrar al EDS": "#fafafa",
    "En proceso": "#f7e62b",
    "No participa": "#D3D3D3",
    "Sin información": SIN_SNSP,

}

# Estilo de los bordes y del resaltado al pasar el cursor.
COLOR_BORDE = "#5A6B7B"
GROSOR_BORDE = 0.7
OPACIDAD_RELLENO = 0.85
COLOR_RESALTADO = "#1F4E5F"
GROSOR_RESALTADO = 2.5
