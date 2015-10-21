<?php
include_once 'dine.php';

$d = new Dine();
# abrir los ambitos para grabarlos en JSON

$do = (array_key_exists('do', $_GET)) ? $_GET['do'] : '';
$do = filter_var($do, FILTER_SANITIZE_ENCODED);
print "DO: " . $do;

if ($do == 'totales_prov' || $do == 'all') {
	$d->totales_prov();
}

if ($do == 'ambitos' || $do == 'all') {
	$d->ambitos();
}

if ($do == 'formulas' || $do == 'all') {
	$d->formulas();
}

if ($do == 'listas' || $do == 'listas') {
	$d->listas();
}

?>