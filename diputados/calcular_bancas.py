from os.path import join
import pandas as pd
from collections import defaultdict

PATH_DATOS_ELECCIONES = "/home/pablo/Proyectos/elecciones2015/resources/datosdeprueba"

HEADERS = {"totaleslistas": 
        ['Código de Elección',
        'Código de Distrito',
        'Código de Sección',
        'Día',
        'Hora',
        'Minuto',
        'Código de agrupación política / fórmula',
        'Votos a la agrupación políticai / fórmula',
        'Porcentaje de votos a la agrupación políticai / fórmula calculados sobre votos positivos válidamente emitidos',
        'Cargos electos'],
        "listas": ['Código de agrupación política / lema / sublema', 'Siglas de agrupación política / lema / sublema', 'Denominación de agrupación política / lema / sublema']
}

def dhondt(dictvotos, nbancas):
    bancas = []
    defaultdict(int)
    cocientes = []
    for codigo, votos in dictvotos.items():
        cocientes += [(codigo, votos/i) for i in range(1, 10)]

    cocientes = sorted(cocientes, key=lambda x: -x[1])

    return cocientes[:nbancas]



def cargar_totales_cba():
    fpath = join(PATH_DATOS_ELECCIONES, 'totaleslistas_04.csv')
    totalescba = pd.read_csv(fpath, delimiter=";")
    totalescba = totalescba.iloc[:,:10]
    totalescba.columns = HEADERS["totaleslistas"]

    return totalescba

def cargar_listas():
    fpath = join(PATH_DATOS_ELECCIONES, 'listas_000.csv')
    listas = pd.read_csv(fpath, delimiter=";", encoding='iso-8859-1')
    listas.columns = HEADERS["listas"]

    return listas

def cargar_votosagrupados():
    totalescba = cargar_totales_cba()
    votosagrup = totalescba[['Votos a la agrupación políticai / fórmula', 'Código de agrupación política / fórmula']].groupby('Código de agrupación política / fórmula').sum()
    
    dictvotos = {}
    for row in votosagrup.iterrows():
        dictvotos[row[0]] = row[1].real[0]

    return dictvotos

if __name__ == '__main__':
    dictvotos = cargar_votosagrupados()
    print("Totales por agrupación")
    for item in dictvotos.items():
        print(item)

    print("=====================")
    print("Asignación de bancas")
    for item in dhondt(dictvotos, nbancas=9):
        print(item)
