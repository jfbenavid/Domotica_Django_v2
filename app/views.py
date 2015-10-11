from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from datetime import datetime
from models import *
from time import sleep
import json

# Create your views here.

def home(request):
	try:
		luz = Luz.objects.all()
		lista = [{'nombre':l.nombre, 'puerto':l.puerto, 'valorLuz':l.valorLuz, 'valorDimmer':l.valorDimmer} for l in luz]
		sJsonLuz = json.dumps(lista)
		template = "index.html"
		return render_to_response(template, locals())
	except Exception, e:
		print "Error en Home: %s" % e
	

def ProcesoLuz(request, id_puerto, valor, tipo):
	try:
		#convertir los parametros en numeros
		iPuerto = int(id_puerto)
		iValor	= int(valor)

		#se consulta el objeto luz que contenga el puerto recibido
		luz = Luz.objects.get(puerto = iPuerto)

		#si el tipo de cambio lo ejecuta el switch de la luz o el dimer
		#luego de eso cambia los valores del objeto luz
		if (tipo == "l"):
			luz.valorLuz = iValor
			luz.valorDimmer = 0 if (luz.valorLuz == 0) else 100
		else:
			luz.valorDimmer = iValor
		
		#guarda los cambios en el objeto
		luz.save()

		#punto de control...
		print "el valor es %d y el puerto es %d el tipo es %s" % (iValor, iPuerto, tipo)
		
		#se envian los datos a la clase ProcesosLuces para que haga el proceso respectivo (dimmer/luz)		
		rpi = ProcesosLuces(iPuerto, iValor)
		rpi.ProcesoRaspberry()
		
		#el objeto cambiado se formatea en un json para retornar a la pagina
		lista = [{'nombre':luz.nombre, 'puerto':luz.puerto, 'valorLuz':luz.valorLuz, 'valorDimmer':luz.valorDimmer}]
		sJsonLuz = json.dumps(lista)
		#punto de control...
		print "aqui volvio al proceso original, el json es: %s" % sJsonLuz

		return HttpResponse(sJsonLuz)

	except Exception, e:
		print "Error en ProcesoLuz: %s" % e