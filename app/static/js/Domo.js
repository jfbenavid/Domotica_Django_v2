var gListaLuz = [];
var gRespuestaLuz = [];
var gsOn  	= '../static/imagenes/botonOn.png';
var gsOff 	= '../static/imagenes/botonOff.png';

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

function mostrarAire() {
	$(".welcome").hide();
	$(".controles").hide();
	$(".infoLuz").hide();
	$(".tablaLuz").hide();
	$(".termometro").show();
}

function mostrarTablaLuz(){
	$(".welcome").hide();
	$(".controles").hide();
	$(".infoLuz").hide();
	$(".termometro").hide();
	$(".tablaLuz").show();
}

function Inicio(){
	InicializarControles();
	SoloNumeros('tTMinima');
	SoloNumeros('tTMaxima');
}

function InicializarControles(){	
	if (gListaLuz.length === 0){
		var hidden = $("#hiddenDb").val();
		gListaLuz = $.parseJSON(hidden);
	}
}

function SoloNumeros (sIdCampo) {
	$('#' + sIdCampo).keydown(function (e) {
		if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 190]) !== -1 || (e.keyCode == 65 && e.ctrlKey === true) || (e.keyCode >= 35 && e.keyCode <= 39)) {
			return;
		}
		if ((e.shiftKey || (e.keyCode < 49 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
			e.preventDefault();
		}
		if ($('#' + sIdCampo).val() > 100){
			e.preventDefault();
		}
	});
}

function cambiarValorPreferencia(sIdCambia, sIdOtro){
	$('#' + sIdOtro).val($('#' + sIdCambia).val());
}

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

//Para encender y apagar las luces, se activa cuando se da click al boton
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

//funciones para manejar el puntero del termometro
// function x2(n,i,x1,r) {return x1 + r * Math.sin(2 * Math.PI * n / i);}
// function y2(n,i,y1,r) {return y1 - r * Math.cos(2 * Math.PI * n / i);}