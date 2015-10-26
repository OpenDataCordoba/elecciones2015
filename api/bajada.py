import requests
import re

from requests.auth import HTTPBasicAuth


resp = requests.get('http://descargas.resultados.gob.ar/desca_nac/descargas.htm', auth=HTTPBasicAuth('DES0062', 'WYYM7329'))
link = "http://descargas.resultados.gob.ar/desca_nac/" + re.findall('a href\=\"(DATOS_\d+.tar.gz)', resp.text)[0]
print link
