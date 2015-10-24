<?php

/**
Datos de la DINE+INDRA el día de las elecciones
*/
class Dine {

	function __construct($base_path_extras = 'datos-de-prueba', $base_path_totales = 'datos-de-prueba') {
		# $this->local_path = '/home/junar/andres/trash/api';
		$this->local_path = 'json';
		$this->base_path_extras = $base_path_extras; # fix el dia de las elecciones
		$this->base_path_totales = $base_path_totales; # fix el dia de las elecciones

		$this->ambitos = $this->base_path_extras . '/ambitos_000.csv';
		$this->formulas = $this->base_path_extras . '/formulas_000.csv';
		$this->listas = $this->base_path_extras . '/listas_000.csv';

		$this->provincias = range(1,24);
		$this->provincias[] = 99; # total nacional

		$this->eleccion = [1=>"Presidente", 2=>"Senadores Nacionales",
							3=>"Diputados Nacionales", 4=>"Gobernador",
							5=>"Senadores Provinciales / Diputados Proporcionales de San Juan",
							6=>"Diputados Provinciales / Diputados Departamentales de San Juan",
							7=>"Concejales de Buenos Aires",
							8=>"Parlasur Nacional", 9=>"Parlasur Provincial"];
	}

	private function read_file($url) {
		$content = file_get_contents($url);
		# $f = fopen($url, 'r');
		# $content = stream_get_contents($f);
		# fclose($f);
		# echo $content;
		$lines = explode("\n", $content);
		return $lines;
	}

	private function write_json($array, $dest) {
		$dest = $this->local_path . '/' . $dest;
		$f = fopen($dest, 'w+');
		fwrite($f, json_encode($array, JSON_PRETTY_PRINT));
		return TRUE;
	}

	# ---- TOTALES 
	function totales_listas() {
		$final = []; # hacer un resumen final para no tener que leer 24 archivos en lo nacional
		foreach ($this->provincias as $prov) {
			$res = [];
			$prov = ($prov < 10 ) ? $prov = "0" . $prov : (string)$prov;
			$lines = $this->read_file($this->base_path_extras . '/totaleslistas_' . $prov . '.csv');
			$this->lg(count($lines) . " lineas en totales prov " . $prov);
			foreach ($lines as $line) {
				$flds = explode(';', $line);
				if (!$flds[0]) continue;
				# print_r($flds); 
				$eleccion = (int)$flds[0];
				$distrito = (int)$flds[1];
				$seccion = (int)$flds[2];
				$idf = $distrito.'_'.$seccion.'_'.$eleccion;
				if (!array_key_exists($idf, $res)) $res[$idf] = [];
				$este = ['dia'=>(int)$flds[3],
						  'hora'=>(int)$flds[4],
						  'minuto'=>(int)$flds[5],
						  'codigo_agrupacion'=>(int)$flds[6],
						  'votos_agrupacion'=>(int)$flds[7],
						  'porc_final_agrupacion'=>(int)$flds[8], # sobre votos validos emitidos
						  'cargos_electos'=>(int)$flds[9],
						  ];

				$res[$idf][] = $este;

				if ($seccion == '999') {
					$este['provincia'] = (int)$prov;
					unset($este['dia']);
					unset($este['hora']);
					unset($este['minuto']);
					if (!array_key_exists($eleccion, $final)){
						$final[$eleccion] = [];
						}

					$final[$eleccion][] = $este;
				
					}

				}

			foreach ($res as $idf => $values) {
		  		$p = explode('_', $idf);
		  		$distrito = $p[0];
		  		$seccion = $p[1];
		  		$eleccion = $p[2];
		  		echo "<br />Totales lisas prov " . $distrito . " - seccion " . $seccion . " - eleccion " . $this->eleccion[$eleccion];
		  		$f = 'totales_listas_' . $distrito . "_" . $seccion . "_" . $eleccion;
				$this->write_json($values, $f . '.json');
				
		  		}
			
			}

		# resultados finales por tipo eleccion (presidente, senadores, etc)
		foreach ($final as $eleccion => $values) {
	  		echo "<br />Totales eleccion " . $this->eleccion[$eleccion];
	  		$f = 'totales_eleccion_' . $eleccion;
			$this->write_json($values, $f . '.json');
	  		}

		return $final;
	}

	# ---- TOTALES 
	function totales_prov() {
		foreach ($this->provincias as $prov) {
			$prov = ($prov < 10 ) ? $prov = "0" . $prov : (string)$prov;
			$lines = $this->read_file($this->base_path_extras . '/totales_' . $prov . '.csv');
			$this->lg(count($lines) . " lineas en totales prov " . $prov);
			foreach ($lines as $line) {
				$flds = explode(';', $line);
				if (!$flds[0]) continue;
				# print_r($flds); 
				$eleccion = (int)$flds[0];
				$distrito = (int)$flds[1];
				$seccion = (int)$flds[2];
				$res = ['mesas_totales'=>(int)$flds[3], 
						  'mesas_escrutadas'=>(int)$flds[4], 
						  'porc_mesas_escrutadas'=>(int)$flds[5],
						  'electores'=>(int)$flds[6],
						  'votantes'=>(int)$flds[7],
						  'participacion_sobre_censo'=>(int)$flds[8],
						  'participacion_sobre_escrutado'=>(int)$flds[9],
						  'electores_escrutados'=>(int)$flds[10],
						  'porc_electores_escrutados'=>(int)$flds[11],
						  'votos_validos'=>(int)$flds[12],
						  'porc_votos_validos'=>(int)$flds[13],
						  'votos_positivos'=>(int)$flds[14],
						  'porc_votos_positivos'=>(int)$flds[15],
						  'votos_en_blanco'=>(int)$flds[16],
						  'porc_votos_en_blanco'=>(int)$flds[17],
						  'votos_nulos'=>(int)$flds[18],
						  'porc_votos_nulos'=>(int)$flds[19],
						  'votos_recurridos_impugnados'=>(int)$flds[20],
						  'porc_votos_recurridos_impugnados'=>(int)$flds[21],
						  'cargos_a_elegir'=>(int)$flds[22],
						  'dia'=>(int)$flds[23],
						  'hora'=>(int)$flds[24],
						  'minuto'=>(int)$flds[25]
						  ];

				# $this->lg("Line " . trim($flds[2]));
			  	echo "<br />Totales prov " . $distrito . " - seccion " . $seccion . " - eleccion " . $this->eleccion[$eleccion];
				$f = 'totales_' . $distrito . "_" . $seccion . "_" . $eleccion;
				$this->write_json($res, $f . '.json');
				
				

				}
			}

		return $res;
	}
	
	# ---- LISTAS 
	function get_listas() {
		$res = [];
		$lines = $this->read_file($this->listas);
		$this->lg(count($lines) . " lineas en listas");
		foreach ($lines as $line) {
			$line = iconv("ISO-8859-1", "UTF-8", $line);
			$flds = explode(';', $line);
			if (!$flds[0]) continue;
			$res[] = ['codigo'=>$flds[0], 'siglas'=>trim($flds[1]), 'denominacion'=>trim($flds[2])];
			# $this->lg("Line " . trim($flds[2]));
		}
		
		return $res;
	}

	function listas(){
		echo "<br />Listas ... ";
		$r = $this->get_listas();
		$this->write_json($r, 'listas.json');
	}


	# ---- AMBITOS 
	function get_ambitos() {
		$res = [];
		$lines = $this->read_file($this->ambitos);
		$this->lg(count($lines) . " lineas en ambitos");
		$myid=0;
		foreach ($lines as $line) {
			$line = iconv("ISO-8859-1", "UTF-8", $line);
			$flds = explode(';', $line);
			if (!$flds[0]) continue;
			$myid++;
			$res[] = ['myid'=>$myid, 'distrito'=>$flds[0], 'subdiv'=>$flds[1], 'subdiv_nombre'=>trim($flds[2])];
			# $this->lg("Line " . trim($flds[2]));
		}
		
		return $res;
	}

	function ambitos(){
		echo "<br />Ambitos ... ";
		$r = $this->get_ambitos();
		$this->write_json($r, 'ambitos.json');
	}

	# ---- FORMULAS 
	function get_formulas() {
		$res = [];
		$lines = $this->read_file($this->formulas);
		$this->lg(count($lines) . " lineas en formulas");
		foreach ($lines as $line) {
			$line = iconv("ISO-8859-1", "UTF-8", $line);
			$flds = explode(';', $line);
			if (!$flds[0]) continue;
			$nombre = trim($flds[2]);
			$nombres = explode(' - ', $nombre);
			$nombres = array_map("trim", $nombres);
			$nombre = join(' - ', $nombres);
			$res[] = ['codigo'=>$flds[0], 'distrito'=>$flds[1], 'nombre'=>$nombre];
			# $this->lg("Line " . trim($flds[2]));
		}
		
		return $res;
	}

	function formulas(){
		echo "<br />Formulas ... ";
		$r = $this->get_formulas();
		$this->write_json($r, 'formulas.json');
	}


	private function lg($txt) {
		echo "<br />" . $txt;
	}
}

?>