from django.shortcuts import render_to_response
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from datetime import datetime
from models import *
from time import sleep
import json
#import RPi.GPIO as GPIO

# Create your views here.

def home(request):
	try:
		luz = Luz.objects.all()
		lista = [{'puerto':l.puerto, 'valorLuz':l.valorLuz, 'valorDimmer':l.valorDimmer} for l in luz]
		sJsonLuz = json.dumps(lista)
		template = "index.html"
		#diccionario = {"luz": luz}
		return render_to_response(template, locals())
	except Exception, e:
		print "Error en Home: %s" % e
	

def ProcesoLuz(request, id_puerto, valor, tipo):
	try:
		iPuerto = int(id_puerto)
		iValor	= int(valor)

		luz = Luz.objects.get(puerto = iPuerto)
		if (tipo == "l"):
			luz.valorLuz = iValor
			luz.valorDimmer = 0 if (luz.valorLuz == 0) else 100
		else:
			luz.valorDimmer = iValor
		
		luz.save()
		print "el valor es %d y el puerto es %d" % (iValor, iPuerto)
		
		#aqui se hace el envio de datos a la clase ProcesosLuces para que haga el proceso respectivo		
		rpi = ProcesosLuces(iPuerto, iValor)
		rpi.ProcesoRaspberry()
		
		lista = [{'puerto':luz.puerto, 'valorLuz':luz.valorLuz, 'valorDimmer':luz.valorDimmer}]
		sJsonLuz = json.dumps(lista)
		print sJsonLuz
		return HttpResponse(sJsonLuz)
	except Exception, e:
		print "Error en ProcesoLuz: %s" % e