## Analisis sobre el padron de las paso 2015

Este padron fue obtenido gracias a que uno de los partidos nos *prestó* el CD
que la justicia electoral le entrego.  

#### Datos generales para Córdoba
2.794.969 electores.  

``` SQL
SELECT secc, circu, mesa, count(*) as total FROM `cordoba` group by secc, circu, mesa order by secc, circu, mesa
```
8411 mesas.  

``` SQL
SELECT secc, circu, count(*) as total FROM `cordoba` group by secc, circu order by secc, circu
```
634 circuitos electorales.  

``` SQL
SELECT secc, count(*) as total FROM `cordoba` group by secc order by secc
```
26 secciones (son los departamentos).  

