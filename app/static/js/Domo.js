var gListaLuz = [];
var gRespuestaLuz = [];
var gsOn  	= '../static/imagenes/botonOn.png';
var gsOff 	= '../static/imagenes/botonOff.png';
var gbIntervalos = false;
var gbValInterval = "";




/*Funcion para mostrar el div del aire acondicionado*/
/*function mostrarAire() {
	$(".welcome").hide();
	$(".controles").hide();
	$(".infoLuz").hide();
	$(".tablaLuz").hide();
	$(".termometro").show();
	sensar();
}*/



/*Funcion que se ejecuta cuando inicia la pagina*/
function Inicio(){
	InicializarControles();

	//si es escritorio o tablet se coloca el sensor a funcionar desde que inicia
	if(screen.width >= 768){
		sensar(); 
	}
}

/*Funcion para cambiar los valores de las preferencias en la base de datos*/
function cambiarValorPreferencia(sIdCambia, sIdOtro){
	$('#' + sIdOtro).text($('#' + sIdCambia).val());
	var tMinima = parseInt($('#tRMinima').val());
	var tMaxima = parseInt($('#tRMaxima').val());
	//var bEstado = $().val();
	$.get('../preferenciasAire/' + tMinima + ' ' + tMaxima + ' 1' /*+ bEstado*/, function(data){
		//alert('Los cambios se han efectuado correctamente');
	});
}



function sensar () {
	gbIntervalos = true
	gbValInterval = setInterval(function (){consultarTemperatura();}, 6000); //se va a poner 300000 para 5 minutos
}

/*Funcion que ejecuta una llamada Ajax a la pagina ejecutarSensor*/
function consultarTemperatura() {
	$.get('../ejecutarSensor/', function(data){
		var gLista = $.parseJSON(data)[0];
		$('#temp').html(gLista.temperatura + " °C");
		$('#humedad').html(gLista.humedad + " %");
	});
}
