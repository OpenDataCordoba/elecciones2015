# -*- coding: utf-8 -*-
"""
leer datos de eolocalizacion de las escuelas en 2013 segun analisis en 
DemocraciaConCodigos 2013 (elecciones legislativas en Córdoba)
democraciaconcodigos.github.io/election-2013/

tomar los datos tambien de las paso 2015 y tratar de cruzar los resultados por escuela

"""

import json
import codecs
import csv

# leer los nombres de los partidos
codigos_partidos_2015 = 'NomPartidos.csv'
partidos = {}
with open(codigos_partidos_2015) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        partidos[row['parCodigo']] = {'siglas': row['parSiglas'].strip(), 'nombre': row['parDenominacion'].strip()}

resultados_presidente_paso_2015 = 'MesasCandidaturaPresidente2015.csv'
secciones = {} # o departamentos
partidos_incluidos = [] # lista de partidos que estan en esta votacion

with open(resultados_presidente_paso_2015) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['vot_depCodigoDepartamento'] not in secciones.keys():
            secciones[row['vot_depCodigoDepartamento']] = {'circuitos': {}}
            print "Create Seccion %s" % row['vot_depCodigoDepartamento']
            
        seccion = secciones[row['vot_depCodigoDepartamento']]
        circuito_num = row['vot_mesCodigoCircuito'].strip().lstrip('0')

        mesa_num = row['vot_mesCodigoMesa'].strip().lstrip('0')
        if circuito_num not in seccion['circuitos'].keys():
            seccion['circuitos'][circuito_num] = {'mesas': {mesa_num: dict()}}
            print "Create Circuito %s" % circuito_num

        circuito = seccion['circuitos'][circuito_num]
        if not mesa_num in circuito['mesas'].keys():
            circuito['mesas'][mesa_num] = dict()
            
        mesa = seccion['circuitos'][circuito_num]['mesas'][mesa_num]


        partido = partidos[row['vot_parCodigo']]['nombre']
        if partido not in partidos_incluidos:
            partidos_incluidos.append(partido)

        mesa[partido] = row['votVotosPartido'] # votos de cada partido en cada mesa
    

with open('paso_2015_por_mesa.csv', 'w') as csvfile:
    fieldnames = ['seccion', 'circuito', 'mesa'] + partidos_incluidos
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for seccion, s in secciones.iteritems():
        for circuito, c in s['circuitos'].iteritems():
            for mesa, m in c['mesas'].iteritems():
                res = {'seccion': seccion, 'circuito': circuito, 
                        'mesa': mesa}
                res.update(m)
                writer.writerow(res)
        
exit()

path='Legislativas-2013-DemocraciaConCodigos.geojson'
f = codecs.open(path, 'r', encoding='utf8')
j = json.load(f)

escuelas =[]

for escuela in j['features']:
    """ samlpe feature
    {"geometry": 
	{"type": "Point", 
	 "coordinates": 
                [-64.18965445684096, -31.414637452814794]
            }, 
        "type": "Feature", 
        "properties": 
	    {"establecim": "CENTRO EDUC.NIVEL MEDIO ADULTO", 
	    "overall_total": 1658, 
	    "fake_id": "1-7", 
	    "seccion": "1", 
	    "circuito": "00001", 
	    "votos": 
	        {"217": 67, "512": 156, "191": 91, "514": 68, "003": 389, "9006": 0, "9005": 26, "9004": 17, "9003": 3, "047": 95, "505": 225, "503": 315, "501": 206}, 
	    "direccion": "DEAN FUNES 417"
            }
    }
    """
    geo = escuela['geometry']
    if geo['type'] != 'Point':
        print "Bad type EXIT"
        exit(1)
        
    lat = geo['coordinates'][0]
    lng = geo['coordinates'][1]

    prop = escuela['properties']
    
    nombre = prop['establecim']
    seccion = prop['seccion']
    circuito = prop['circuito'].lstrip('0')
    direccion = prop['direccion'] or ''
    votos = prop['votos']
    mesa_desde, mesa_hasta = prop['fake_id'].split('-')
    
    """ votos
    var listNames = {
         '003': ['UCR','#ff0000'],
         '047':['CCV','#0b4c5f'],
         '191':['VINDEP','#ff00ff'],
         '217':['EVC','#fe9a2e'],
         '501': ["FPV", '#3ea1d2'],
         '503': ["Union PRO", '#ebe126'],
         '504': ['AUC','#ffbf00'],
         '505': ['FIT', '#ab181f'],
         '512':['UPC','#04b486'],
         '514':['FPCyS','#08298a'],
         '9003':['Impugnados','#b18904'],
         '9004':['Blancos','#ffffff'],
         '9005':['Nulos','#a4a4a4'],
         '9006':['Recurridos','#31b404']
    }
    """
    total_votos = prop['overall_total']
    esta = {'nombre': nombre, 'direccion': direccion, 'seccion': seccion, 
            'circuito': circuito, 'lat': lat, 'lng': lng, 'votos': total_votos,
            'mesa_desde': mesa_desde, 'mesa_hasta': mesa_hasta}
    escuelas.append(esta)

f = codecs.open('escuelas-geo-elecciones-2013-cordoba.csv', 'w', encoding='utf8')
f.write('Seccion,Circuito,Escuela,Direccion,votos,Mesa desde, Mesa hasta,Lat,Long\n')
for data in escuelas:
    print str(data)
    tpl = (data['seccion'], data['circuito'] , data['nombre'].replace(',', '.') , 
            data['direccion'].replace(',', '.') , data['votos'] , 
            data['mesa_desde'], data['mesa_hasta'],
            data['lat'], data['lng'] )
    f.write('%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % tpl)

f.close()
print "END"

    
    

    
    