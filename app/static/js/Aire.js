gConfig = []

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
		glista = $.parseJSON(usarAjaxGet('../ejecutarSensor/'));
		/*$.get('../ejecutarSensor/', function(data){
			var gLista = $.parseJSON(data);
			$('#temp').html(gLista.temperatura + " °C");
			$('#humedad').html(gLista.humedad + " %");
		});*/
	}
	else{
		glista = $.parseJSON(usarAjaxGet('../temperaturaAuto/' + $('select[id=preferencia]').val()));
		/*$.get('../temperaturaAuto/' + $('select[id=preferencia]').val(), function(data){
			var gLista = $.parseJSON(data);
			$('#temp').html(gLista.temperatura + " °C");
			$('#humedad').html(gLista.humedad + " %");
		});*/
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
}

function Inicio () {
	InicializarControles();
	
	$('select[id=preferencia]').change(function(){cambiarPreferencia(2);});

	setInterval(function (){
		sensarTemperatura();
	}, 6000);
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

function controlManual (control) {
	var boton = "";
	if (control == 1)
		boton = "key_power";
	else if(control == 2)
		boton = "key_volumeup";
	else if(control == 3)
		boton = "key_volumedown";
	else if(control == 4)
		boton = "key_slow";
	else
		alert('Error en pulsar un boton del control manual!');
	
	usarAjaxGet('../controlManual/' + boton);
	/*$.get('../controlManual/' + boton, function (data) {
		//alert('el control se cambio');
	});*/
}
