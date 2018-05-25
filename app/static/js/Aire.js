gConfig = []
configAire = {
	temperaturas: { '16':'KEY_TEMPERATURE16', '17':'KEY_TEMPERATURE17', '18':'KEY_TEMPERATURE18', '19':'KEY_TEMPERATURE19', '20':'KEY_TEMPERATURE20', '21':'KEY_TEMPERATURE21', '22':'KEY_TEMPERATURE22', '23':'KEY_TEMPERATURE23', '24':'KEY_TEMPERATURE23', '25':'KEY_TEMPERATURE23' },
	estado: {'apagar' : 'powerOff', 'encender': 'powerOn'}
}

function usarAjaxGet (ruta) {
	var retorno;
	$.get(ruta, function (data) {
		retorno = data;
	})
	return retorno;
}

function cambiarPreferencia (control) {
	var retorno = usarAjaxGet('../preferenciasAire/' + control + ' ' + $('select[id=preferencia]').val());
	/*$.get('../preferenciasAire/' + control + ' ' + $('select[id=preferencia]').val(), function (data) {
		//alert('el control se cambio');
	});*/
}

function cambioControl (esconder, mostrar, normal, negrita){
	$(esconder).hide();
	$(mostrar).show();
	$(negrita).css('font-weight','bold');
	$(normal).css('font-weight','normal');
}

/*Funcion que ejecuta una llamada Ajax a la pagina ejecutarSensor*/
function sensarTemperatura() {
	var glista;
	if ($('input:radio[id=usoManual]:checked').val() == 1) {
		$.get('../ejecutarSensor/', function(data){
			var gLista = $.parseJSON(data);
			$('#temp').html(gLista.temperatura + " °C");
			$('#humedad').html(gLista.humedad + " %");
		});
	}
	else{
		$.get('../temperaturaAuto/' + $('select[id=preferencia]').val(), function(data){
			var gLista = $.parseJSON(data);
			$('#temp').html(gLista.temperatura + " °C");
			$('#humedad').html(gLista.humedad + " %");
		});
	}
}

function InicializarControles () {
	if (gConfig.length === 0){
		var hidden = $("#hiddenDb").val();
		gConfig = $.parseJSON(hidden);
	}
	
	$('#preferencia option[value=' + gConfig.preferencia + ']').prop('selected',true);

	if(gConfig.control == 1){
		cambioControl('.aireAutomatico','.aireManual','#lAuto','#lManual');
		$('#usoManual').attr('checked', true);
	}
	else{
		cambioControl('.aireManual','.aireAutomatico','#lManual','#lAuto');
		$('#usoAuto').attr('checked', true);
	}

	var textoEstado = gConfig.estado ? 'Encendido.' : 'Apagado.';
	$('#estado').text(textoEstado);

	$('#tempActual').text(gConfig.temperatura);
}

function Inicio () {
	InicializarControles();
	
	$('select[id=preferencia]').change(function(){cambiarPreferencia(2);});

	setInterval(function (){
		sensarTemperatura();
	}, 300000);
}

function switchControles (control) {
	if (control == 'manual') {
		cambioControl('.aireAutomatico','.aireManual','#lAuto','#lManual');
		cambiarPreferencia(1);
	}
	else{
		cambioControl('.aireManual','.aireAutomatico','#lManual','#lAuto');
		cambiarPreferencia(2);
	}
}

function ControlEstado (estado) {
	if (!estado) {
		$('#estado').text('Encendido.');
		controlManual(configAire.estado.encender, 1, 1);
		$('#power').attr('onclick', 'ControlEstado(true)');
	} else{
		$('#estado').text('Apagado.');
		controlManual(configAire.estado.apagar, 1, 0);
		$('#power').attr('onclick', 'ControlEstado(false)');
	}
}

function subirTemperatura () {
	var actual = parseInt($('#tempActual').text());
	if (actual < 25 && actual > 15) {
		actual++;
		$('#tempActual').text(actual);
		controlManual(configAire.temperaturas[actual.toString()], 2, actual);
	}
}

function bajarTemperatura () {
	var actual = parseInt($('#tempActual').text());
	if (actual < 26 && actual > 16) {
		actual--;
		$('#tempActual').text(actual);
		controlManual(configAire.temperaturas[actual.toString()], 2, actual);
	}
}

function controlManual (control, tipo, estadoTemp) {
	usarAjaxGet('../controlManual/' + control + ' ' + tipo + ' ' + estadoTemp);
	//$.get('../controlManual/' + control + ' ' + tipo + ' ' + estadoTemp, function (data) {
		//alert(data);
	//});
}
