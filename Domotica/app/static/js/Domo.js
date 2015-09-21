var gListaLuz = [];
var gsOn  	= '../static/imagenes/botonOn.png';
var gsOff 	= '../static/imagenes/botonOff.png';

function CambiarVista(){
	var select = $.trim($('.Seleccione').text());
	if(select!=="Seleccione"){
		$('#welcome').hide();
		$('#control').show();
	}
	else{
		$('#control').hide();
		$('#welcome').show();
	}
}

//para el combobox
function clickcaja(e) {
	var lista = $(this).find("ul"),
		triangulo = $(this).find("span:last-child");
	e.preventDefault();
	//lista.is(":hidden") ? $(this).find("ul").show() : $(this).find("ul").hide();
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
	$("#hiddenPuerto").val(texto);
	InicializarControles();
	CambiarVista();
	lista.hide();
	triangulo.removeClass("triangulosup").addClass("trianguloinf");
}

function Inicio(){
	$(".cajaselect").click(clickcaja);
	$(".cajaselect").on("click", "li", clickli);
}

function InicializarControles(){	
	if (gListaLuz.length === 0){
		var hidden = $("#hiddenDb").val();
		gListaLuz = $.parseJSON(hidden);
	}
	$("#hiddenPuerto").val($("#hiddenPuerto").val().replace("Puerto", ""));
	//$("#hiddenPuerto").val(puerto);
	var iPuerto = parseInt($("#hiddenPuerto").val());
	for (var i = 0; i < gListaLuz.length; i++) {
		if (gListaLuz[i].puerto == iPuerto) {
			$("#imgOnOff").attr("src", (gListaLuz[i].valorLuz === 1) ? gsOn : gsOff);
			$("#idDimmer").val(gListaLuz[i].valorDimmer);
		}
	}
}

//Para encender y apagar las luces, se activa cuando se da click al boton
function ProcesoLuz(control){
	var puerto	= parseInt($("#hiddenPuerto").val());
	for (var i = 0; i < gListaLuz.length; i++) {
		if (gListaLuz[i].puerto == puerto) {
			if (control == "luz") {
				gListaLuz[i].valorLuz = (gListaLuz[i].valorLuz === 1) ? 0 : 1;
				$('#imgOnOff').attr('src', (gListaLuz[i].valorLuz === 1) ? gsOn : gsOff);
				$.get('ProcesoLuz/' + puerto + ' ' + gListaLuz[i].valorLuz + ' l', function(data){
					alert('muy bien la luz!');
				});
			}
			else{
				gListaLuz[i].valorDimmer = parseInt($("#idDimmer").val());
				$.get('ProcesoLuz/' + puerto + ' ' + gListaLuz[i].valorDimmer + ' d', function(data){
					alert('muy bien el dimmer!');
				});
			}
			break;
		}
	}
}