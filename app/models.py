from django.db import models
import threading
import logging
import time
#import sys
#import Adafruit_DHT
#import RPi.GPIO as GPIO

nombreHilo = {}

class Luz(models.Model):
	nombre = models.CharField(max_length = 60, default = "")
	puerto = models.IntegerField(default = 0)
	valorLuz = models.IntegerField(default = 0)
	valorDimmer = models.IntegerField(default = 0)
	
	def __unicode__(self):
		return "Nombre: %s - Puerto: %s - EstadoLuz: %s - ValorDimmer: %s" % (self.nombre, self.puerto, self.valorLuz, self.valorDimmer)

	class Meta:
		ordering = ['puerto']

class Aire(models.Model):
	puerto = models.IntegerField(default = 0)
	temperaturaMinima = models.IntegerField(default = 0)
	temperaturaMaxima = models.IntegerField(default = 0)
	estado = models.IntegerField(default = 0)

	def __unicode__(self):
		return "Puerto: %s - Temperatura Maxima: %s - Temperatura Minima: %s - Estado: %s" % (self.puerto, self.temperaturaMaxima, self.temperaturaMinima, self.estado)

class ProcesosLuces():
	def __init__(self, idPuerto, valor, estadoHilo = True):
		self.puerto = int(idPuerto)
		self.valor = int(valor)
		nombreHilo['puerto' + str(self.puerto)] = bool(estadoHilo)

	def ProcesarLuz(self):
		print "Entro al metodo ProcesarLuz: [puerto: %s][valor: %s]" % (self.puerto, self.valor)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.puerto, GPIO.OUT)
		bOnOff = True

		if (self.valor == 1):
			bOnOff = False

		GPIO.output(self.puerto, bOnOff)

	def ProcesarDimmer(self):
	#aqui se hace el proceso de la luz en el puerto de la raspberry
		frecuencia = 0

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.puerto, GPIO.OUT)
		#cambia la frecuencia para la etapa de potencia
		if self.valor >= 40 and self.valor <= 60:
			frecuencia = 60
		elif self.valor == 70:
			frecuencia = 80
		else:
			frecuencia = 100

		#debido a que el transistor es inverso se debe cambiar el ciclo
		self.valor = 100 - self.valor

		l = GPIO.PWM(self.puerto, frecuencia)
		l.start(100)
		try:
			while nombreHilo['puerto' + str(self.puerto)]:
				l.ChangeDutyCycle(self.valor)
				time.sleep(0.1)
			print "se finalizo el metodo ProcesarDimmer del puerto %s" % self.puerto
		except Exception, e:
			l.stop()
			GPIO.cleanup()
			print "Error en ProcesosLuces/ProcesoRaspberry: %s" % e

class ProcesosTemperatura():
	def __init__(self, prueba = 0):
		self.prueba = prueba

	def SensarTodo(self):
		try:
			#el 11 representa que es el DHT11 (si fuera el DHT22 se coloca 22); el 4 representa el numero del puerto
			humedad, temperatura = Adafruit_DHT.read_retry(11, 4) 
			aire = Aire.objects.get(puerto = 4)
			bCambiar = True

			if (temperatura < aire.temperaturaMinima or temperatura > aire.temperaturaMaxima):
				if bCambiar:
					GPIO.setmode(GPIO.BCM)
					GPIO.setup(26, GPIO.OUT) #el puerto 26 es el definido para el aire acondicionado
					GPIO.output(26, True)
					bCambiar = False
			else:
				GPIO.setmode(GPIO.BCM)
				GPIO.setup(26, GPIO.OUT) #el puerto 26 es el definido para el aire acondicionado
				GPIO.output(26, False)
				bCambiar = True

			return humedad, temperatura

		except Exception, e:
			print "Hubo un error en SensarTodo() - %s" % e