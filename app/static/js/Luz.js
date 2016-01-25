var gListaLuz = [];
var gRespuestaLuz = [];
var gsOn  	= '../static/imagenes/botonOn.png';
var gsOff 	= '../static/imagenes/botonOff.png';

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

function Inicio(){
	InicializarControles();
}

/*guarda lo que trae el servidor y lo coloca dentro de una variable global*/
function InicializarControles(){	
	if (gListaLuz.length === 0){
		var hidden = $("#hiddenDb").val();
		gListaLuz = $.parseJSON(hidden);
	}
}

/*Funcion que se ejecutara cada vez que se seleccione un puerto*/
function luzOverClick (puerto) {
	$("#hiddenPuerto").val(puerto);
	CambiosEstados();
	$(".luzOver").css('background','none');
	if(screen.width <= 900){
		$(".controles").show();
		$(".infoLuz").show();
		$(".tablaLuz").hide();	
	}
	else{
		$("#puertoLuz" + puerto).css('background','rgba(0,0,0,0.1)');
	}
}

/*Para encender y apagar las luces, se activa cuando se da click al boton*/
function ProcesoLuz(control){
	var puerto	= parseInt($("#hiddenPuerto").val());
	for (var i = 0; i < gListaLuz.length; i++) {
		if (gListaLuz[i].puerto == puerto) {
			if (control == "luz") {
				var sLuz = (gListaLuz[i].valorLuz == 1) ? " 0" : " 1";
				$.get('../ProcesoLuz/' + puerto + sLuz + ' l', function(data){
					gListaLuz[i] = $.parseJSON(data)[0];
					CambiosEstados();
					alert('muy bien la luz!' + gListaLuz[i].valorLuz);
				});
			}
			else{
				$.get('../ProcesoLuz/' + puerto + ' ' + parseInt($("#idDimmer").val()) + ' d', function(data){
					gListaLuz[i] = $.parseJSON(data)[0];
					CambiosEstados();
					alert('muy bien el dimmer!' + gListaLuz[i].valorDimmer);
				});
			}
			break;
		}
	}
}