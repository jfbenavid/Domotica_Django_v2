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
		print "Error en Home"
	

def ProcesoLuz(request, id_puerto, valor, tipo):
	try:
		iPuerto = int(id_puerto)
		iValor	= int(valor)

		luz = Luz.objects.get(puerto = iPuerto)
		if (tipo == "l"):
			luz.valorLuz = iValor
		else:
			luz.valorDimmer = iValor
		luz.save()
		print "el valor es %d y el puerto es %d" % (iValor, iPuerto)
		
		#self.ProcesoRaspberry(iPuerto, iValor)

		return HttpResponseRedirect("/")
	except Exception, e:
		print "Error en ProcesoLuz"

#def ProcesoRaspberry(self, id_puerto, valor):
	#aqui se hace el proceso de la luz en el puerto de la raspberry
	#try:
		#GPIO.setmode(GPIO.BCM)
		#GPIO.setup(iPuerto, GPIO.OUT)
		#l = GPIO.PWM(iPuerto, iValor)
		#l.start(0)
		#try:
		#	while True:
		#		l.ChangeDutyCycle(iValor)
		#except Exception, e:
		#	l.stop()
		#	GPIO.cleanup()
		#	print "hubo un problema en la luz " + e.message
	#except Exception, e:
	#	print "Error en ProcesoRaspberry"