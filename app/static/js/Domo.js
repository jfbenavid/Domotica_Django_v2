var gListaLuz = [];
var gRespuestaLuz = [];
var gsOn  	= '../static/imagenes/botonOn.png';
var gsOff 	= '../static/imagenes/botonOff.png';

function luzOverClick (puerto) {
	if(screen.width < 768){
		$("#hiddenPuerto").val(puerto);
		CambiosEstados();
		$(".controles").show();
		$(".infoLuz").show();
		$(".tablaLuz").hide();	
	}
}

//para el combobox
function clickcaja(e) {
	var lista = $(this).find("ul"),
		triangulo = $(this).find("span:last-child");
	e.preventDefault();
	$(this).find("ul").toggle();
	if(lista.is(":hidden")) {
		triangulo.removeClass("triangulosup").addClass("trianguloinf");
	}
	else {
		triangulo.removeClass("trianguloinf").addClass("triangulosup");
	}
}

function mostrarTablaLuz(){
	$(".welcome").hide();
	$(".controles").hide();
	$(".infoLuz").hide();
	$(".tablaLuz").show();
}

//para el combobox
function clickli(e) {
	var texto = $(this).text(),
		seleccionado = $(this).parent().prev(),
		lista = $(this).closest("ul"),
		triangulo = $(this).parent().next();
	e.preventDefault();
	e.stopPropagation();    
	seleccionado.text(texto);
	//se coloca el numero de puerto en el hidden para procesar
	for (var i = 0; i < gListaLuz.length; i++) {
		if (texto.trim() === gListaLuz[i].nombre) {
			$("#hiddenPuerto").val(gListaLuz[i].puerto);
			break;
		}
	}
	CambiosEstados();
	CambiarVista();
	lista.hide();
	triangulo.removeClass("triangulosup").addClass("trianguloinf");
}

function Inicio(){
	$(".cajaselect").click(clickcaja);
	$(".cajaselect").on("click", "li", clickli);
	InicializarControles();
}

function InicializarControles(){	
	if (gListaLuz.length === 0){
		var hidden = $("#hiddenDb").val();
		gListaLuz = $.parseJSON(hidden);
	}
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
			$("#estadoPuerto" + iPuerto).text(gListaLuz[i].valorLuz);
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