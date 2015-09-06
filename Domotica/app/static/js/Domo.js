var estado 	= 0;

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
	$("#hiddenPuerto").val(seleccionado.text());
	CambiarVista();
	lista.hide();
	triangulo.removeClass("triangulosup").addClass("trianguloinf");
}

function Inicio(){
	$(".cajaselect").click(clickcaja);
	$(".cajaselect").on("click", "li", clickli);
}

//Para encender y apagar las luces, se activa cuando se da click al boton
function OnOff(){
	var on  	= '../static/imagenes/botonOn.png';
	var off 	= '../static/imagenes/botonOff.png';
	var listaPuerto	= ($("#hiddenPuerto").val()).split(" ");
	var puerto  = listaPuerto[1];

	if(estado === 0){
		$('#imgOnOff').attr('src', on);
		estado = 1;
	}
	else{
		$('#imgOnOff').attr('src', off);
		estado = 0;
	}
	$.get('Enciende/' + parseInt(puerto) + ' ' + estado + ' l', function(data){
		alert('muy bien!');
	});
}





