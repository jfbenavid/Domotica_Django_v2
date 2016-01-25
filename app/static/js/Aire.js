gConfig = []

function cambiarPreferencia (control) {
	$.get('../preferenciasAire/' + control + ' ' + $('select[id=preferencia]').val(), function (data) {
		alert('el control se cambio');
	});
}

function cambioControl (esconder, mostrar, normal, negrita){
	$(esconder).hide();
	$(mostrar).show();
	$(negrita).css('font-weight','bold');
	$(normal).css('font-weight','normal');
}

/*Funcion que ejecuta una llamada Ajax a la pagina ejecutarSensor*/
function sensarTemperatura() {
	if ($('input:radio[name=uso]:checked').val() == 1) {
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
}

function Inicio () {
	InicializarControles();
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


