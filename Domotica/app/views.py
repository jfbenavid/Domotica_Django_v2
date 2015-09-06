from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from datetime import datetime
from models import *
from time import sleep
#import RPi.GPIO as GPIO

# Create your views here.

def home(request):
	luz = Luz.objects.all()
	template = "index.html"
	#diccionario = {"luz": luz}
	return render_to_response(template, locals())

def Enciende(request, id_puerto, valor, tipo):
	iPuerto = int(id_puerto)
	luz = Luz.objects.get(puerto = iPuerto)
	if (tipo == "l"):
		luz.ValorLuz = valor
	else:
		luz.ValorDimmer = valor
	luz.save()
	#aqui se hace el proceso de la luz en el puerto de la raspberry
#	GPIO.setmode(GPIO.BCM)
#	GPIO.setup(iPuerto, GPIO.OUT)
#	l = GPIO.PWM(iPuerto, valor)
#	l.start(0)
#	try:
#		while True:
#			l.ChangeDutyCycle(valor)
#	except Exception, e:
#		l.stop()
#		GPIO.cleanup()
#		print "hubo un problema en la luz " + e.message
	
	return HttpResponseRedirect("/")

