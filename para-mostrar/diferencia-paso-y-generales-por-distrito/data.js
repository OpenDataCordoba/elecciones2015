
/**
Leer los datos de las elecciones y comparar
*/

// var bp = 'http://opendatacordoba.org/elecciones2015/api/json';
var bp = '../../api/json';

var url_provincias = bp + '/provincias_full.json';

// candidaturas finales
var url_formulas = bp + '/formulas.json'; // el ganador de cada formula solamente
var url_listas = bp + '/listas.json' // nombres de los partidos 
// resultados de las paso por alianza por distrito
// PROVISORIO !!! var url_paso = bp + '/PASO-2015-totales-por-provincia-Alinazas-sin-lemas.json';
var url_paso = bp + '/PASO-DEF2015-totales-por-provincia-Alinazas-sin-lemas.json';
var url_definitva = bp + '/totales_eleccion_1_test.json'; // 1 es eleccion presidencial

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
			prov[provincia.codigo] = provincia; //{'nombre': provincia.provincia};
		});

		var f = {}; // formulas
		$.each(formulas[0], function(k, formula){
			codigo = parseInt(formula.codigo);
			if (formula.distrito == "99"){ // solo las formulas presidenciales
				f[codigo] = {'nombre': formula.nombre, 'distrito': formula.distrito};
				}
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
			if (paso.provincia != 99) p[paso.alianza][99].votos = p[paso.alianza][99].votos + paso.votos;
		});

		var d = {}; // eleccion definitiva
		$.each(definitivas[0], function(k, definitiva){
			if (undefined === d[definitiva.codigo_agrupacion]){
				d[definitiva.codigo_agrupacion] = {};
			}
			d[definitiva.codigo_agrupacion][definitiva.provincia] = definitiva.votos_agrupacion;
			if (undefined == prov[definitiva.provincia]['votaron_def']) {
				prov[definitiva.provincia]['votaron_def'] = 0;
			}
			// saber cuantos votaron en la definitiva para proyectar
			prov[definitiva.provincia]['votaron_def'] = prov[definitiva.provincia]['votaron_def'] + definitiva.votos_agrupacion;
			// actualizar el porc que voto
			votaron_def_porc = prov[definitiva.provincia]['votaron_def'] / prov[definitiva.provincia]['votos_positivos'];
			prov[definitiva.provincia]['votaron_def_porc'] = 100 * votaron_def_porc;
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
		// variaciones de alianzas en provincias
		var alidef = {};
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
					res2[prov_id] = {"nombre": prov[prov_id].provincia};
				}
				votos_def_porc = 100 * definitiva_tot / prov[prov_id].votaron_def;
				res2[prov_id]['alianza_' + alianza] = l[alianza].nombre;
				res2[prov_id]['votos_paso_' + alianza] = votos.votos;
				res2[prov_id]['votos_paso_porc_' + alianza] = votos.porc;
				res2[prov_id]['votos_def_' + alianza] = definitiva_tot;
				res2[prov_id]['votos_def_porc' + alianza] = votos_def_porc;
				var def_proyectado = definitiva_tot * (100/prov[prov_id].votaron_def_porc);
				res2[prov_id]['votos_def_proyectado_' + alianza] = def_proyectado;
				diff = def_proyectado - votos.votos;
				res2[prov_id]['votos_def_diff_' + alianza] = diff;

				// solo las listas que van ahora
				if (def_proyectado > 0){
					if (undefined === alidef[alianza]){
						alidef[alianza] = {'alianza': l[alianza], 'formula': f[alianza]};
					}

					var diff_contra_nacional = 100 * diff / prov[99].votos_positivos;
					var este = {'provincia': prov[prov_id].provincia,
								'paso': votos.votos,
								'paso_porc': votos.porc,
								'definitivas': definitiva_tot,
								'definitivas_porc': Math.round(votos_def_porc * 100) / 100,
								'definitivas_proyectado': Math.round(def_proyectado),
								'diferencia': Math.round(diff),
								'aporte_nacional': Math.round(diff_contra_nacional * 100) / 100 }
					alidef[alianza][prov_id] = este;
					}
				});
		});
		console.log(res2);

		console.log(alidef);
		
		$.each(alidef, function(alianza, info){
			$('#resultados').append('<h2>'+alianza+': '+info['alianza'].nombre+'</h2>');
			$('#resultados').append('<h3>'+info['formula'].nombre+'</h3>');
			$alianza_table = $('#resultados').append('<table class="results" id="alianza_'+alianza+'"></table>');
			$alianza_table.append('<tr><th>Provincia</th><th>Paso</th><th>Ahora</th><th>Proyectado</th><th>Diferencia</th><th>Var Nacional</th></tr>');
			// total nacional
			nac = '<tr><td>Total Nacional</td><td>'+info[99].paso+' ('+info[99].paso_porc+' %)</td>';
			nac += '<td>'+info[99].definitivas+' ('+info[99].definitivas_porc+' %)</td><td>'+info[99].definitivas_proyectado+'</td>';
			nac += '<td>'+info[99].diferencia+'</td><td>'+info[99].aporte_nacional+'</td></tr>';
			$alianza_table.append(nac);
			
			for(var i=1; i<25; i++){
				pr = '<tr><td>'+info[i].provincia+'</td><td>'+info[i].paso+' ('+info[i].paso_porc+' %)</td>';
				pr += '<td>'+info[i].definitivas+' ('+info[i].definitivas_porc+' %)</td><td>'+info[i].definitivas_proyectado+'</td>';
				pr += '<td>'+info[i].diferencia+'</td><td>'+info[i].aporte_nacional+'</td></tr>';
				$alianza_table.append(pr);
				
			}
			

		});
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