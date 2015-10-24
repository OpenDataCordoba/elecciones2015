from collections import OrderedDict
import pandas as pd

from bokeh._legacy_charts import Bar, output_file, show
from bokeh.palettes import YlGn3 as PALETTE


URL_TOTALES_PRESIDENTE = 'http://opendatacordoba.org/elecciones2015/api/json/totales_eleccion_1.json'

URL_LISTAS = 'http://opendatacordoba.org/elecciones2015/api/json/listas.json'

def get_plot_data():
    df = pd.read_json(URL_TOTALES_PRESIDENTE)
    totales = df[df.provincia == 99]
    totales.sort('porc_final_agrupacion', ascending=False)

    codigos = totales.codigo_agrupacion.values
    porcentajes = totales.porc_final_agrupacion.astype(float).values
    porcentajes *= 0.01

    primero, segundo = porcentajes[:2]

    if primero >= 45:
        falta = 0
    else:
        falta = max(40 , (segundo + 10)) - primero

    faltante = [0] * len(porcentajes)
    faltante[0] = falta

    listas = pd.read_json(URL_LISTAS)
    def get_siglas_lista(c):
        return listas[listas.codigo == c].siglas.values[0]

    siglas = [get_siglas_lista(c) for c in codigos]

    return siglas, (porcentajes, faltante)

siglas, (porcentajes, faltante) = get_plot_data()

# build a dict containing the grouped data
data = [porcentajes, faltante]

output_file("primervueltometro.html")

# Flyer derecho fijo : 300 x 500
# Zonas de columna auxiliar : 300 x 300 (1er y 2do rolado)
# Puente largo : 975 x 80
# Puente corto : 650 x 80
width, height = 300, 300

z = 2
width *= z
height *= z

params = {
    "title": "Primer Vueltómetro",
    "stacked": True,
    "width": width,
    "height": height,
    "tools": "",
    "palette": PALETTE
}

bar = Bar(data, siglas, **params)

show(bar)
