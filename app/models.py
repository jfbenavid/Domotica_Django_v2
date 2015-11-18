from django.db import models
import threading
import logging
import time
import RPi.GPIO as GPIO

nombreHilo = {}

class Propietarios(models.Model):
	nombre = models.CharField(max_length = 100)
	usuario = models.CharField(max_length = 20)
	contrasena = models.CharField(max_length = 20)

	def __unicode__(self):
		return "Nombre: %s - User: %s - Pass: %s" % (self.nombre, self.usuario, self.contrasena)

class Luz(models.Model):
	nombre = models.CharField(max_length = 60)
	puerto = models.IntegerField(default = 0)
	valorLuz = models.IntegerField(default = 0)
	valorDimmer = models.IntegerField(default = 0)
	
	def __unicode__(self):
		return "Nombre: %s - Puerto: %s - EstadoLuz: %s - ValorDimmer: %s" % (self.nombre, self.puerto, self.valorLuz, self.valorDimmer)

class ProcesosLuces():
	def __init__(self, idPuerto, valor, estadoHilo = True):
		self.puerto = int(idPuerto)
		self.valor = int(valor)
		nombreHilo['puerto' + str(self.puerto)] = bool(estadoHilo)

	def ProcesarLuz(self):
		#print "Entro al metodo ProcesarLuz: [puerto: %s][valor: %s]" % (self.puerto, self.valor)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.puerto, GPIO.OUT)
		bOnOff = False

		if (self.valor == 1):
			bOnOff = True

		GPIO.output(self.puerto, bOnOff)

	def ProcesarDimmer(self):
		# while nombreHilo['puerto' + str(self.puerto)]:
		# 	print "este hilo es el del puerto %s y tiene %d porciento" % (self.puerto,self.valor)
		#aqui se hace el proceso de la luz en el puerto de la raspberry
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.puerto, GPIO.OUT)
		l = GPIO.PWM(self.puerto, 100)
		l.start(100)
		try:
			while nombreHilo['puerto' + str(self.puerto)]:
				l.ChangeDutyCycle(self.valor)
				time.sleep(0.1)
			print "aqui se ejecuto todo bien en el metodo ProcesarDimmer .l."
		except Exception, e:
			luz.stop()
			GPIO.cleanup()
			print "Error en ProcesosLuces/ProcesoRaspberry: %s" % e



