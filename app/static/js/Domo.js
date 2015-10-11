var gListaLuz = [];
var gRespuestaLuz = [];
var gsOn  	= '../static/imagenes/botonOn.png';
var gsOff 	= '../static/imagenes/botonOff.png';

function CambiarVista(){
	var select = $.trim($('.Seleccione').text());
	if(select!=="Seleccione"){
		$('.welcome').hide();
		$('.controles').show();
		$('.infoLuz').show();
	}
	else{
		$('.infoLuz').hide();
		$('.controles').hide();
		$('.welcome').show();
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
	//InicializarControles();
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
	//$("#hiddenPuerto").val($("#hiddenPuerto").val().replace("Puerto", ""));
	//CambiosEstados();
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