from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from datetime import datetime
from models import *
import json
import threading
import logging
import time


# Create your views here.
def home(request):
	try:
		luz = Luz.objects.all()
		lista = [{'nombre':l.nombre, 'puerto':l.puerto, 'valorLuz':l.valorLuz, 'valorDimmer':l.valorDimmer} for l in luz]
		sJsonLuz = json.dumps(lista)
		aire = Aire.objects.get(puerto = 4)
		template = "index.html"
		return render_to_response(template, locals())
	except Exception, e:
		print "Error en Home: %s" % e

def preferenciasAire(request, tMinimo, tMaximo, estado):
	try:
		iTempMinima = int(tMinimo)
		iTempMaxima = int(tMaximo)

		aire = Aire.objects.get(puerto = 4)
		aire.temperaturaMinima = iTempMinima
		aire.temperaturaMaxima = iTempMaxima
		aire.estado = estado
		aire.save()

		lista = [{'tMinima':aire.temperaturaMinima, 'tMaxima':aire.temperaturaMaxima, 'valorLuz':aire.estado}]
		sJsonLuz = json.dumps(lista)

		return HttpResponse(sJsonLuz)

	except Exception, e:
		raise e

def ProcesoLuz(request, idPuerto, valor, tipo):
	try:
		#convertir los parametros en numeros
		iPuerto = int(idPuerto)
		iValor	= int(valor)

		#se consulta el objeto luz que contenga el puerto recibido
		luz = Luz.objects.get(puerto = iPuerto)

		#si el tipo de cambio lo ejecuta el switch de la luz o el dimer
		#luego de eso cambia los valores del objeto luz
	
		if (tipo == "l"):
			luz.valorLuz = iValor
			if (luz.valorLuz == 0):
				luz.valorDimmer = 0
				#se crea objeto de la clase ProcesosLuces con los valores de los parametros
				rpi = ProcesosLuces(iPuerto, iValor, False)

			else:
				luz.valorDimmer = 100
				rpi = ProcesosLuces(iPuerto, iValor)
					
			rpi.ProcesarLuz()
		else:
			rpi = ProcesosLuces(iPuerto, iValor, False)
			time.sleep(0.05)
			luz.valorDimmer = iValor
			if (luz.valorDimmer != 100): 
				rpi = ProcesosLuces(iPuerto, iValor)
			else:
				return ProcesoLuz(iPuerto, 100, 'l')

			hiloDimmer = threading.Thread(target = rpi.ProcesarDimmer, name = 'dimmer' + str(iPuerto))
			hiloDimmer.setDaemon(True)
			hiloDimmer.start()
		
		#guarda los cambios en el objeto
		luz.save()

		#el objeto cambiado se formatea en un json para retornar a la pagina
		lista = [{'nombre':luz.nombre, 'puerto':luz.puerto, 'valorLuz':luz.valorLuz, 'valorDimmer':luz.valorDimmer}]
		sJsonLuz = json.dumps(lista)

		return HttpResponse(sJsonLuz)

	except Exception, e:
		print "Error en ProcesoLuz: %s" % e