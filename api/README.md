# PHP API

Para leer los CSV de DINE+INDRA y sacar Json listos para usar.  
  
#### Releer los totales por provincia, seccion y eleccion  
http://opendatacordoba.org/elecciones2015/api/?do=totales_prov

Esto genera un json por cada provincia, seccion y eleccion
Por ejemplo:
*Presidenciales en Cordoba, depto Colon*  
http://opendatacordoba.org/elecciones2015/api/json/totales_4_3_1.json  
Donde 4 es cordoba, 3 es el depto Colon (ver ambitos) y 1 es el codigo de la eleccion a presidente
Codigos de eleccion
```
	1=>"Presidente", 2=>"Senadores Nacionales",
	3=>"Diputados Nacionales", 4=>"Gobernador",
	5=>"Senadores Provinciales / Diputados Proporcionales de San Juan",
	6=>"Diputados Provinciales / Diputados Departamentales de San Juan",
	7=>"Concejales de Buenos Aires",
	8=>"Parlasur Nacional", 9=>"Parlasur Provincial"
```

Los totales departamentales se informan como *seccion* 999, entonces el total de Córdoba para presidente es:  
http://opendatacordoba.org/elecciones2015/api/json/totales_4_999_1.json  
  
Los totales presidenciales se informan como *distrito* 99 y *seccion* 999, entonces el total nacional para presidente es:  
http://opendatacordoba.org/elecciones2015/api/json/totales_99_999_1.json  


#### Releer los ambitos
http://opendatacordoba.org/elecciones2015/api/?do=ambitos  
Luego se leen desde: 
http://opendatacordoba.org/elecciones2015/api/json/ambitos.json  

#### Releer las formulas
http://opendatacordoba.org/elecciones2015/api/?do=formulas  
Luego se leen desde: 
http://opendatacordoba.org/elecciones2015/api/json/formulas.json  

#### Releer las listas
http://opendatacordoba.org/elecciones2015/api/?do=listas  
Luego se leen desde: 
http://opendatacordoba.org/elecciones2015/api/json/listas.json  

