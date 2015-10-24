# -*- coding: utf-8 -*-
"""
leer todos los CSVs derivados del PDF de resultados oficiales
"""
import sys
import csv
provincias = range(1,25)
provincias.append(99)

res = {}

def clean(s):
    try:
        ret = int(s.replace('.', '').strip())
    except Exception, e:
        print "*************\ncant decode (%s) %s\n***************\n" % (s, str(e))
        raise
        
    return ret
    
def clean_porc(s):
    try:
        ret = float(s.replace('%', '').replace(',', '.').strip())
    except Exception, e:
        print "*************\ncant decode (%s) %s\n***************\n" % (s, str(e))
        raise
    
    return ret

votos_positivos_total = 0
electores_total = 0
alianzas = [131, 135, 138, 132, 137, 133, 136, 13, 134, 81, 57]
lemas = {'131': ['3166'],
         '135': ['3182', '3185', '3243'],
         '138': ['3192', '3214'],
         '132': ['3008'],
         '137': ['3014', '3261'],
         '133': ['3100'],
         '136': ['3234'],
         '13': ['3253'],
         '134': ['3018'],
         '81': ['3217'],
         '57': ['3172']
         }

for p in provincias:
    res[p] = {}
    
    with open('%d.csv' % p) as csvfile:
        print "PROVINCIA: %d" % p
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        rows = list(reader)

        if rows[0][1].strip() != "ELECTORES HABILES":
            print "BAD DATA %d (%s)" % (p, rows[0][1])
            sys.exit()

        res[p]['electores'] = clean(rows[0][2])
        res[p]['mesas'] = clean(rows[1][2])
        res[p]['porc_voto'] = clean_porc(rows[2][2])

        res[p]['votos_positivos'] = clean(rows[30][2])
        res[p]['votos_blanco'] = clean(rows[31][2])
        res[p]['votos_anulados'] = clean(rows[32][2])
        res[p]['votos_total'] = clean(rows[33][2])

        res[p]['131'] = {'total': clean(rows[4][2])}
        res[p]['131']['porc'] = clean_porc(rows[4][3])
        res[p]['131']['3166'] = clean(rows[4][2])
        
        res[p]['135'] = {'total': clean(rows[6][2])}
        res[p]['135']['porc'] = clean_porc(rows[6][3])
        res[p]['135']['3182'] = clean(rows[7][2])
        res[p]['135']['3185'] = clean(rows[8][2])
        res[p]['135']['3243'] = clean(rows[9][2])

        # check
        if res[p]['135']['total'] != res[p]['135']['3182'] + res[p]['135']['3185'] + res[p]['135']['3243']:
            print "BAD DATA 135"
            sys.exit()
        
        res[p]['138'] = {'total': clean(rows[10][2])}
        res[p]['138']['porc'] = clean_porc(rows[10][3])
        res[p]['138']['3192'] = clean(rows[11][2])
        res[p]['138']['3214'] = clean(rows[12][2])
        res[p]['132'] = {'3008': clean(rows[13][2]), 'total': clean(rows[13][2])}
        res[p]['132']['porc'] = clean_porc(rows[13][3])
        
        res[p]['137'] = {'total': clean(rows[15][2])}
        res[p]['137']['porc'] = clean_porc(rows[15][3])
        res[p]['137']['3014'] = clean(rows[16][2])
        res[p]['137']['3261'] = clean(rows[17][2])
        res[p]['133'] = {'3100': clean(rows[18][2]), 'total': clean(rows[18][2])}
        res[p]['133']['porc'] = clean_porc(rows[18][3])
        
        res[p]['136'] = {'3234': clean(rows[20][2]), 'total': clean(rows[20][2])}        
        res[p]['136']['porc'] = clean_porc(rows[20][3])
        
        res[p]['13'] = {'3253': clean(rows[22][2]), 'total': clean(rows[22][2])}
        res[p]['13']['porc'] = clean_porc(rows[22][3])
        
        res[p]['134'] = {'3018': clean(rows[24][2]), 'total': clean(rows[24][2])}
        res[p]['134']['porc'] = clean_porc(rows[24][3])
        
        res[p]['81'] = {'3217': clean(rows[26][2]), 'total': clean(rows[26][2])}
        res[p]['81']['porc'] = clean_porc(rows[26][3])
        
        res[p]['57'] = {'3172': clean(rows[28][2]), 'total': clean(rows[28][2])}
        res[p]['57']['porc'] = clean_porc(rows[28][3])
        

        # check general
        votos_positivos = 0
        for a in alianzas:
            votos_positivos += res[p][str(a)]['total']
        if votos_positivos != res[p]['votos_positivos']:
            print "BAD total"
            sys.exit()

        porc = 0
        for a in alianzas:
            porc += res[p][str(a)]['porc']
            
        if porc < 99 or porc > 101:
            print "BAD porc"
            sys.exit()

        if votos_positivos != res[p]['votos_positivos']:
            print "BAD total"
            sys.exit()


        if p != 99:
            votos_positivos_total += votos_positivos
            electores_total += res[p]['electores']

for p in provincias:
    print "Electores %d: %d" % (p, res[p]['electores'])
    print "Votos positivos %d: %d" % (p, res[p]['votos_positivos'])


# revisar totales
if electores_total != res[99]['electores']:
    print "BAD FULL electores total"
    print electores_total
    print res[99]['electores']
    sys.exit()

if votos_positivos_total != res[99]['votos_positivos']:
    print "BAD FULL votos total"
    print votos_positivos_total
    print res[99]['votos_positivos']
    sys.exit()

# totales sin lemas
sinlema = []
for p in provincias:
    for a in alianzas:
        sinlema.append({"provincia":p,"alianza":a,"votos":res[p][str(a)]['total'],"porc":res[p][str(a)]['porc']})

print "**********\nSin Lemas\n**********\n"
print str(sinlema)

conlema = []
for p in provincias:
    for a, lema in lemas.iteritems():
        for l in lema:
            conlema.append({"provincia":p,"alianza":a, "lema": l, "votos":res[p][str(a)][l]})

print "**********\nCon Lemas\n**********\n"
print str(conlema)


import json
f = open('PASO-DEF2015-totales-por-provincia-Alinazas-sin-lemas.json', 'w')
json.dump(sinlema, f, indent=4)
f.close()

f = open('PASO-DEF2015-totales-por-provincia-Alinazas-con-lemas.json', 'w')
json.dump(conlema, f, indent=4)
f.close()
        
    