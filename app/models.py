from django.db import models
import threading
import logging
import time

#importante para las funcionalidades dentro de la raspberry
#import sys
#import Adafruit_DHT
#import RPi.GPIO as GPIO

nombreHilo = {}		#para manejar los hilos del dimmer

#creacion y uso de la base de datos
class Luz(models.Model):
	nombre = models.CharField(max_length = 60, default = "")
	puerto = models.IntegerField(default = 0, unique = True)
	valorLuz = models.IntegerField(default = 0)
	valorDimmer = models.IntegerField(default = 0)
	
	def __unicode__(self):
		return "Nombre: %s - Puerto: %s - EstadoLuz: %s - ValorDimmer: %s" % (self.nombre, self.puerto, self.valorLuz, self.valorDimmer)

	#Clase usada para ordenar por el campo que se desea al hacer consultas por orm
	class Meta:
		ordering = ['puerto']

class Aire(models.Model):
	puerto = models.IntegerField(default = 0)
	temperaturaMinima = models.IntegerField(default = 0)
	temperaturaMaxima = models.IntegerField(default = 0)
	estado = models.IntegerField(default = 0)

	def __unicode__(self):
		return "Puerto: %s - Temperatura Maxima: %s - Temperatura Minima: %s - Estado: %s" % (self.puerto, self.temperaturaMaxima, self.temperaturaMinima, self.estado)

#Clase usada para el manejo de las luces (encendido/apagado y dimmer)
class ProcesosLuces():
	def __init__(self, idPuerto, valor, estadoHilo = True):
		self.puerto = int(idPuerto)
		self.valor = int(valor)
		nombreHilo['puerto' + str(self.puerto)] = bool(estadoHilo)

	#Metodo para encendido y apagado de luces
	def ProcesarLuz(self):
		print "Entro al metodo ProcesarLuz: [puerto: %s][valor: %s]" % (self.puerto, self.valor)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.puerto, GPIO.OUT)

		bOnOff = True 	#para apagar, false para encender debido al transistor que se usa ya que este es inverso

		if (self.valor == 1):
			bOnOff = False

		GPIO.output(self.puerto, bOnOff)

	#Metodo para dimerizar las luces
	def ProcesarDimmer(self):
		frecuencia = 0 	#Cantidad de hertz con la que funcionara el dimmer

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.puerto, GPIO.OUT)
		
		#Debido a que el transistor es inverso se debe cambiar el ciclo
		self.valor = 100 - self.valor

		#Cambia la frecuencia para la etapa de potencia
		if self.valor >= 40 and self.valor <= 60:
			frecuencia = 60
		elif self.valor == 70:
			frecuencia = 80
		else:
			frecuencia = 100

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

#Clase para el sensado de temperatura y humedad
class ProcesosTemperatura():
	def __init__(self, prueba = 0):
		self.prueba = prueba

	def SensarTodo(self):
		try:
			#el 11 representa que es el DHT11 (si fuera el DHT22 se coloca 22); el 4 representa el numero del puerto
			humedad, temperatura = Adafruit_DHT.read_retry(11, 4) #Sensa la humedad y la temperatura
			aire = Aire.objects.get(puerto = 4) 	#obtiene el objeto con puerto=4 en la base de datos
			bCambiar = True

			#Si la temperatura esta entre el rango de preferencias apague el puerto 26 de lo contrario prendalo
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