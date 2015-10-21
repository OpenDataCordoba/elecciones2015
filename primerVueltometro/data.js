$.getJSON( '../api/json/totales_listas_99_999_1.json', function( data ) {
	var total = 0;
	$.each( data, function( k, lista ) {
		total += lista.votos_agrupacion;
		});
 	alert("TOTAL " + total);
  
});