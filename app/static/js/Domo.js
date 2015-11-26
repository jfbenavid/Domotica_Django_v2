var gListaLuz = [];
var gRespuestaLuz = [];
var gsOn  	= '../static/imagenes/botonOn.png';
var gsOff 	= '../static/imagenes/botonOff.png';
var gbIntervalos = false;
var gbValInterval = "";

/*Funcion que se ejecutara cada vez que se seleccione un puerto*/
function luzOverClick (puerto) {
	$("#hiddenPuerto").val(puerto);
	CambiosEstados();
	$(".luzOver").css('background','none');
	if(screen.width <= 768){
		$(".controles").show();
		$(".infoLuz").show();
		$(".tablaLuz").hide();	
	}
	else{
		$("#puertoLuz" + puerto).css('background','rgba(0,0,0,0.1)');
	}
}

/*Funcion para mostrar el div del aire acondicionado*/
function mostrarAire() {
	$(".welcome").hide();
	$(".controles").hide();
	$(".infoLuz").hide();
	$(".tablaLuz").hide();
	$(".termometro").show();
	sensar();
}

/*Funcion para mostrar la tabla de puertos de luz*/
function mostrarTablaLuz(){
	$(".welcome").hide();
	$(".controles").hide();
	$(".infoLuz").hide();
	$(".termometro").hide();
	$(".tablaLuz").show();
	if(gbIntervalos == true){
		clearInterval(gbValInterval);
	}
}

/*Funcion que se ejecuta cuando inicia la pagina*/
function Inicio(){
	InicializarControles();

	//si es escritorio o tablet se coloca el sensor a funcionar desde que inicia
	if(screen.width >= 768){
		sensar(); 
	}
}

/*guarda lo que trae el servidor y lo coloca dentro de una variable global*/
function InicializarControles(){	
	if (gListaLuz.length === 0){
		var hidden = $("#hiddenDb").val();
		gListaLuz = $.parseJSON(hidden);
	}
}

/*Funcion para cambiar los valores de las preferencias en la base de datos*/
function cambiarValorPreferencia(sIdCambia, sIdOtro){
	$('#' + sIdOtro).text($('#' + sIdCambia).val());
	var tMinima = parseInt($('#tRMinima').val());
	var tMaxima = parseInt($('#tRMaxima').val());
	//var bEstado = $().val();
	$.get('preferenciasAire/' + tMinima + ' ' + tMaxima + ' 1' /*+ bEstado*/, function(data){
		alert('Los cambios se han efectuado correctamente');
	});
}

/*cambia el contenido de los estados en la tabla*/
function CambiosEstados(){
	var iPuerto = parseInt($("#hiddenPuerto").val());
	for (var i = 0; i < gListaLuz.length; i++) {
		if (gListaLuz[i].puerto == iPuerto) { 
			if (gListaLuz[i].valorLuz === 1) {
				$("#imgOnOff").attr("src", gsOn);
				$("#idDimmer").removeAttr("disabled");
			}
			else{
				$("#imgOnOff").attr("src", gsOff);
				$("#idDimmer").attr("disabled", "disabled");
			}
			$("#estadoPuerto" + iPuerto).text((gListaLuz[i].valorLuz == 1) ? "Encendido" : "Apagado");
			$("#valorDimmer" + iPuerto).text(gListaLuz[i].valorDimmer);
			$("#idDimmer").val(gListaLuz[i].valorDimmer);
			$(".port").text("Puerto " + gListaLuz[i].puerto);
			$(".infoEstadoDimmer").text("Dimmer en " + gListaLuz[i].valorDimmer + "%");
			$(".infoEstadoOnOff").text((gListaLuz[i].valorLuz == 1) ? "Energia On" : "Energia Off");
			break;
		}
	}
}

/*Para encender y apagar las luces, se activa cuando se da click al boton*/
function ProcesoLuz(control){
	var puerto	= parseInt($("#hiddenPuerto").val());
	for (var i = 0; i < gListaLuz.length; i++) {
		if (gListaLuz[i].puerto == puerto) {
			if (control == "luz") {
				var sLuz = (gListaLuz[i].valorLuz == 1) ? " 0" : " 1";
				$.get('ProcesoLuz/' + puerto + sLuz + ' l', function(data){
					gListaLuz[i] = $.parseJSON(data)[0];
					CambiosEstados();
					alert('muy bien la luz!' + gListaLuz[i].valorLuz);
				});
			}
			else{
				$.get('ProcesoLuz/' + puerto + ' ' + parseInt($("#idDimmer").val()) + ' d', function(data){
					gListaLuz[i] = $.parseJSON(data)[0];
					CambiosEstados();
					alert('muy bien el dimmer!' + gListaLuz[i].valorDimmer);
				});
			}
			break;
		}
	}
}

function sensar () {
	gbIntervalos = true
	gbValInterval = setInterval(function (){consultarTemperatura();}, 6000); //se va a poner 300000 para 5 minutos
}

/*Funcion que ejecuta una llamada Ajax a la pagina ejecutarSensor*/
function consultarTemperatura() {
	$.get('ejecutarSensor/', function(data){
		var gLista = $.parseJSON(data)[0];
		$('#temp').html(gLista.temperatura + " °C");
		$('#humedad').html(gLista.humedad + " %");
	});
}
