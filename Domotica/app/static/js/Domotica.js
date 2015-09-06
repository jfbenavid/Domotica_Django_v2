//variables globales
estado = 0
on = 'imagenes/botonOn.png';
off = 'imagenes/botonOff.png';
var x = null;

function Iniciar(){
	
	CargarDatos();
	$('#fancyClock').tzineClock();
	//en click cambie el boton de on a off
	$('.imagen').click(OnOff);
	$('#puerto').bind('keydown change', MostrarPuerto);
	$('#puerto').change(CargarDatos);
}

function MostrarPuerto(){
	$('.port').text("Puerto seleccionado: " + $('#puerto').val());
}
//funcion para cambiar el boton de "on" a "off"
function OnOff(){ 
	//$(this).attr('src',($(this).attr('src') === on)?off:on);
	x = getPuerto();
	if(x != null){
		$('onOff').fadeToggle('explode');
		$('onOff').css({'display':'block'});
		$(this).attr('src',function(){
			if($(this).attr('src') === on){
				$(this).attr('src', off);
				estado = 0;
			}else{
				$(this).attr('src', on);
				estado = 1;
			}
		});
	}
}

function IniciarOnOff(){
	x = getPuerto();
	var resp;
	if(x != null){
		$.post('php/consulta_luz.php',{port: x}, function(resp){
			this.resp = resp; 
		});
	}
}

function getPuerto(){
	return $('#puerto').val();
}

function EstadoDimmer(){
	var valEstado = $('#idDimmer').val();
	var puerto = getPuerto();

	$.post('php/procesa_dimmer.php',{estado: valEstado, puerto: puerto, tipoConsul: 2},function(resp){
		//cambia el valor del dimmer mostrado en pagina
			$('.infoEstadoDimmer').text("Dimmer en " + resp + "%");
			$('#idDimmer').val(resp);
	});
}

function CargarDatos(){
	var valEstado = $('#idDimmer').val();
	var puerto = getPuerto();

	$.post('php/procesa_dimmer.php',{estado: valEstado, puerto: puerto, tipoConsul: 1},function(resp){
		//cambia el valor del dimmer mostrado en pagina
			$('.infoEstadoDimmer').text("Dimmer en " + resp + "%");
			$('#idDimmer').val(resp);
	});
}
});
