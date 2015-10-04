# -*- coding: utf-8 -*-
""" Leer el copiado y pegado """

import codecs

path='Carta-Marina-2015-PDFTOTEX-LAYOUT.txt'

f = codecs.open(path, 'r', encoding='utf8')
raw=f.read()

""" 
el archivo tiene estas propiedades (se copio y pego directo del PDF a texto, tabula no funciono bien)
Esta linea es la primera de alguna páginas
La mesa 5829 va en realidad en realidad en 
ESCUELA N°359 - WASHINGTON Circuito 193 - TOSQUITA 

"""

lines = raw.split('\n')

# valores actuales que cambian cada x escuelas
seccion_nro = 0
seccion_name = ''
circuito_nro = '' # NO ES NUMERICO
circuito_name=''

imin = '' # en que estoy
cnt = 0
errores=0

escuelas = [] # resultados finales
last_mesa= 0 # controlar que todos los numeros de mesa esten incluidos

for r in lines:
    cnt += 1
    
    if r.find(u'                      Página') > -1:
        print 'NO - PAGE'
        continue

    if r.strip() == u'DISTRITO CORDOBA':
        print 'NO - DIST'
        continue

    if r.find(u'              ELECCIONES 2015') > -1:
        print 'NO - ELEC'
        continue

    if r.find(u'      Informe de Establecimientos') > -1:
        print 'NO - INFO'
        continue
        
    if r.find(u'Sección ') == 0: # es la seccion
        p = r.replace(u'Sección ', u'').strip().split('-')
        seccion_nro = int(p[0].strip())
        seccion_name = p[1].strip()
        print "Empezando seccion %d %s" % (seccion_nro, seccion_name)
        prev_line = r
        imin = ''
        continue

    if r.find(u' Circuito') == 0: # es la seccion
        p = r.replace(u' Circuito', u'').strip().split('-')
        circuito_nro = p[0].strip()
        p2 = p[1].split('       ') # en la misma linea hay titulos de otros campos mas abajo
        circuito_name = p2[0].strip()
        print "Empezando circuito %s %s" % (circuito_nro, circuito_name)
        prev_line = r
        imin = 'escuelas' # marco que estoy en las escuelas
        continue

    if r == '' or r.find(u'Resúmen del Circuito') == 0:
        imin = ''
        continue
    
    if imin == 'escuelas':
        p = r.split('    ')
        p2 = [x for x in p if x.strip() != ''] # tomar solo los datos reales
        print "%d -- %s" % (cnt, str(p2))
        escuela = p2[0]
        cant_mesas = int(p2[1])
        mesa_desde = int(p2[2].split(' a ')[0])
        if mesa_desde != last_mesa + 1:
            print "Mesa invalida %d %d" % (mesa_desde, last_mesa)
            exit(1)
        mesa_hasta = int(p2[2].split(' a ')[1])
        last_mesa = mesa_hasta
        cant_electores = int(p2[3].replace('.', ''))
        print "Escuela %s. %d mesas. Desde %d a %d. %d electores" % (escuela, cant_mesas, mesa_desde, mesa_hasta, cant_electores)
        elem = {'seccion_nro': seccion_nro,
                'seccion_name': seccion_name,
                'circuito_nro': circuito_nro,
                'circuito_name': circuito_name,
                'escuela': escuela.replace(',', '.'),
                'cant_mesas': cant_mesas,
                'desde': mesa_desde, 'hasta': mesa_hasta,
                'electores': cant_electores}
        escuelas.append(elem)
        continue

print "Escuelas: %d" % len(escuelas)

f = codecs.open('escuelas-elecciones-2015-cordoba.csv', 'w', encoding='utf8')
f.write('Seccion Nro,Seccion Nombre,Circuito Nro,Circuito Nombre,Escuela,Mesas,Desde,Hasta,Electores\n')
for data in escuelas:
    escuela = data['escuela']
    seccion_nro = data['seccion_nro']
    seccion_name = data['seccion_name']
    circuito_nro = data['circuito_nro']
    circuito_name = data['circuito_name']
    cant_mesas = data['cant_mesas']
    desde = data['desde']
    hasta = data['hasta']
    electores = data['electores']

    f.write('%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % (seccion_nro, seccion_name, circuito_nro, circuito_name, 
                                                 escuela, cant_mesas, desde, hasta, electores))

f.close()
print "END"
