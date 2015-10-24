
/**
Leer los datos de las elecciones y comparar
*/

// var bp = 'http://opendatacordoba.org/elecciones2015/api/json';
var bp = '../../api/json';

var url_provincias = bp + '/provincias.json';

// candidaturas finales
var url_formulas = bp + '/formulas.json'; // el ganador de cada formula solamente
var url_listas = bp + '/listas.json' // nombres de los partidos 
// resultados de las paso por alianza por distrito
// PROVISORIO !!! var url_paso = bp + '/PASO-2015-totales-por-provincia-Alinazas-sin-lemas.json';
var url_paso = bp + '/PASO-DEF2015-totales-por-provincia-Alinazas-sin-lemas.json';
var url_definitva = bp + '/totales_eleccion_1.json'; // 1 es eleccion presidencial

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

getData = function(url){
	return $.getJSON(url);
};

getBaseData = function(){
	provincias = getData(url_provincias);
	listas = getData(url_listas);
	formulas = getData(url_formulas);
	pasos = getData(url_paso);
	definitivas = getData(url_definitva);
	
	$.when(provincias, formulas, listas, pasos, definitivas).done(function(provincias, formulas, listas, pasos, definitivas){
		var prov = {99: {'nombre': 'Total Nacional'} }; // formulas
		$.each(provincias[0], function(k, provincia){
			prov[provincia.codigo] = {'nombre': provincia.provincia};
		});

		var f = {}; // formulas
		$.each(formulas[0], function(k, formula){
			codigo = parseInt(formula.codigo);
			f[codigo] = {'nombre': formula.nombre, 'distrito': formula.distrito};
		});


		var l = {}; // listas
		$.each(listas[0], function(k, lista){
			codigo = parseInt(lista.codigo);
			l[codigo] = {'nombre': lista.denominacion};
		});


		var p = {}; // paso
		$.each(pasos[0], function(k, paso){
			if (undefined === p[paso.alianza]){
				p[paso.alianza] = {99: {'votos':0, 'porc': 100}}; // no tiene acumulados, crearlos
				}
			if (paso.provincia == 88) {
				p[paso.alianza][2].votos = p[paso.alianza][2].votos + paso.votos;
				}
			else {
				if (undefined === p[paso.alianza][paso.provincia])
					{
					p[paso.alianza][paso.provincia] = {};		
					}
				p[paso.alianza][paso.provincia]['votos'] = paso.votos;
				p[paso.alianza][paso.provincia]['porc'] = paso.porc;
				}
			p[paso.alianza][99].votos = p[paso.alianza][99].votos + paso.votos;
		});

		var d = {}; // eleccion definitiva
		$.each(definitivas[0], function(k, definitiva){
			if (undefined === d[definitiva.codigo_agrupacion]){
				d[definitiva.codigo_agrupacion] = {};
			}
			d[definitiva.codigo_agrupacion][definitiva.provincia] = definitiva.votos_agrupacion;
		});

		console.log(prov);
		console.log(f);
		console.log(l);
		console.log(p);
		console.log(d);
		
		// hacer tabla comparativa
		// por alianzas
		var res = [];
		$.each(p, function(alianza, provs){
			$.each(provs, function(prov_id, votos){
				// puede no haber pasado !
				prov_id = parseInt(prov_id);
				if (undefined === d[alianza]) {
					definitiva_tot = 0;
				}
				else {
					definitiva_tot = d[alianza][prov_id];
				}
				if (undefined === res[alianza]){
					res[alianza] = {"nombre": l[alianza].nombre, "votos": []};
				}
				res[alianza].votos[prov_id] = {"provincia": prov[prov_id].nombre, 
												"paso": votos, 
												"definitivas": definitiva_tot};

				});
		});
		console.log(res);

		// por provincias
		var res2 = [];
		$.each(p, function(alianza, provs){
			$.each(provs, function(prov_id, votos){
				// puede no haber pasado !
				prov_id = parseInt(prov_id);
				if (undefined === d[alianza]) {
					definitiva_tot = 0;
				}
				else {
					definitiva_tot = d[alianza][prov_id];
				}
				if (undefined === res2[prov_id]){
					res2[prov_id] = {"nombre": prov[prov_id].nombre};
				}
				res2[prov_id]['alianza_' + alianza] = l[alianza].nombre;
				res2[prov_id]['votos_paso_' + alianza] = votos.votos;
				res2[prov_id]['votos_paso_porc_' + alianza] = votos.porc;
				res2[prov_id]['votos_def_' + alianza] = definitiva_tot;
				// ponderar estos parciales segun el porcentaje

				
				});
		});
		console.log(res2);

		

		$('#resultados').append('');
	});

	


}

$(function() {
  getBaseData();
});

/*
var xhr = $.getJSON(url_paso, function(data){
	var total = 0;
	$.each( data, function( k, lista ) {
		total += lista.votos_agrupacion;
		});
 	alert("TOTAL " + total);
});
var paso_por_distrito 
*/