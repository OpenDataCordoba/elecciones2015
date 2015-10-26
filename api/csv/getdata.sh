echo "*******************"
echo "Generales"
echo "*******************"
# wget --post-data 'user=DS0062&password=WYYM7329' http://descargas.resultados.gob.ar/desca_nac/generales_000.tar.gz
# wget --user=DS0062 --password=WYYM7329 http://descargas.resultados.gob.ar/desca_nac/generales_000.tar.gz
# wget --http-user=DS0062 --http-password=WYYM7329 http://descargas.resultados.gob.ar/desca_nac/generales_000.tar.gz
wget http://DES0062:WYYM7329@descargas.resultados.gob.ar/desca_nac/generales_000.tar.gz
tar xvzf generales_000.tar.gz

echo "*******************"
echo "Datos"
echo "*******************"
#wget --post-data 'user=DS0062&password=WYYM7329' http://descargas.resultados.gob.ar/desca_nac/DATOS_20193448.tar.gz
# wget --user=DS0062 --password=WYYM7329 http://descargas.resultados.gob.ar/desca_nac/DATOS_20193448.tar.gz
# wget --http-user=DS0062 --http-password=WYYM7329 http://descargas.resultados.gob.ar/desca_nac/DATOS_20193448.tar.gz
wget http://DES0062:WYYM7329@descargas.resultados.gob.ar/desca_nac/DATOS_20193448.tar.gz
tar xvzf DATOS_20193448.tar.gz

mv DATOS_20193448/* .
mv generales_000/* .
