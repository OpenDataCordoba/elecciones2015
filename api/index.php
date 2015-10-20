<?php
include_once 'dine.php';

$d = new Dine();
# abrir los ambitos para grabarlos en JSON

if ($_GET['do'] == 'ambitos' || $_GET['do'] == 'all') {
	$d->ambitos();
}

if ($_GET['do'] == 'formulas' || $_GET['do'] == 'all') {
	$d->formulas();
}

if ($_GET['do'] == 'listas' || $_GET['do'] == 'listas') {
	$d->listas();
}

?>