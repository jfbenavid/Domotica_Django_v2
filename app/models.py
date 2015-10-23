from django.db import models
import threading
import logging
import time
#import RPi.GPIO as GPIO

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
	def __init__(self, id_puerto, valor):
		self.puerto = int(id_puerto)
		self.valor = int(valor)

	def ProcesarLuz(self):
		print "Entro al metodo ProcesarLuz: [puerto: %s][valor: %s]" % (self.puerto, self.valor)
		# GPIO.setmode(GPIO.BCM)
		# GPIO.setup(self.puerto, GPIO.OUT)
		# bOnOff = False

		# if (self.valor == 1):
		# 	bOnOff = True

		# GPIO.output(self.puerto, bOnOff)

	def ProcesarDimmer(self):
		while True:
			print "este ciclo infinito se ejecuta en segundo plano"
		#aqui se hace el proceso de la luz en el puerto de la raspberry
		# GPIO.setmode(GPIO.BCM)
		# GPIO.setup(self.puerto, GPIO.OUT)
		# l = GPIO.PWM(self.puerto, 100)
		# l.start(100)
		# try:
		# 	while True:
		# 		l.ChangeDutyCycle(self.valor)
		# 		time.sleep(0.1)
		# 	print "aqui se ejecuto todo bien en el metodo ProcesarDimmer .l."
		# except Exception, e:
		# 	luz.stop()
		# 	GPIO.cleanup()
		# 	print "Error en ProcesosLuces/ProcesoRaspberry: %s" % e