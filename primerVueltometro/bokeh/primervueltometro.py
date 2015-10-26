from collections import OrderedDict
import pandas as pd

from bokeh._legacy_charts import Bar, output_file, show
from bokeh.palettes import YlGn3 as PALETTE

from utils import json_dump_unicode

CANDIDATOS = {
    "ALIANZA UNIDOS POR UNA NUEVA ALTERNATIVA (UNA)": "Massa",
    "ALIANZA FRENTE DE IZQUIERDA Y DE LOS TRABAJADORES": "Del Caño",
    "ALIANZA CAMBIEMOS": "Macri",
    "ALIANZA FRENTE PARA LA VICTORIA": "Scioli",
    "ALIANZA PROGRESISTAS": "Stolbizer",
    "ALIANZA COMPROMISO FEDERAL": "Rodríguez Saa"
}

URL_TOTALES_PRESIDENTE = 'http://opendatacordoba.org/elecciones2015/api/json/totales_eleccion_1.json'

URL_LISTAS = 'http://opendatacordoba.org/elecciones2015/api/json/listas.json'

def get_plot_data():
    df = pd.read_json(URL_TOTALES_PRESIDENTE)
    totales = df[df.provincia == 99]
    totales.sort('porc_final_agrupacion', ascending=False)

    codigos = totales.codigo_agrupacion.values
    porcentajes = totales.porc_final_agrupacion.astype(float).values
    porcentajes *= 0.01
    porcentajes = list(porcentajes)

    primero, segundo = porcentajes[:2]

    # if primero >= 45:
    #     falta = 0

    falta = max(40 , (segundo + 10)) - primero

    listas = pd.read_json(URL_LISTAS)
    def get_candidatos_lista(c):
        return listas[listas.codigo == c].siglas.values[0]

    fuerzas = [get_candidatos_lista(c) for c in codigos]
    candidatos =  [CANDIDATOS[f] for f in fuerzas]
    
    data = (candidatos, (porcentajes, falta))
    json_dump_unicode(data, "databokeh.json")
    
    return data

def create_plot():
    candidatos, (porcentajes, falta) = get_plot_data()

    if falta <= 0:
        sobra = -falta
        fserie = [sobra] + [0] * 5
        porcentajes[0] -= sobra
        resultado = "Gana %s en Primera Vuelta" % candidatos[0]
        data = OrderedDict([("porcentajes", porcentajes), ("sobra", fserie)])
    else:
        fserie = [falta] + [0] * 5
        resultado = "Hay Ballotage"
        data = OrderedDict([("porcentajes", porcentajes), ("falta", fserie)])


    # build a dict containing the grouped data

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
        "title": "PrimerVueltómetro: %s" % resultado,
        "stacked": True,
        "width": width,
        "height": height,
        "tools": "",
        "palette": PALETTE,
        "legend": 'top_right'
    }

    bar = Bar(data, candidatos, **params)

    show(bar)

if __name__ == '__main__':
    create_plot()