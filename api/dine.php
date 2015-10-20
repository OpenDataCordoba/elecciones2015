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

	# ---- LISTAS 
	function get_listas() {
		$res = [];
		$lines = $this->read_file($this->listas);
		$this->lg(count($lines) . " lineas en listas");
		foreach ($lines as $line) {
			$flds = explode(';', $line);
			if (!$flds[0]) continue;
			$res[] = ['codigo'=>$flds[0], 'siglas'=>trim($flds[1]), 'denominacion'=>trim($flds[2])];
			# $this->lg("Line " . trim($flds[2]));
		}
		
		return $res;
	}

	function listas(){
		echo "<br />Formulas ... ";
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