from django.db import models
from subprocess import call
import threading
import logging
import time

#lo siguiente es importante para las funcionalidades dentro de la raspberry
# import sys
# import Adafruit_DHT	#Para el sensado de temperatura
# import RPi.GPIO as GPIO	#Para poder utilizar los puertos GPIO

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
	control = models.IntegerField(default = 1)
	preferencia = models.IntegerField(default = 1)
	puerto = models.IntegerField(default = 0)
	temperaturaControl = models.IntegerField(default = 17)
	estado = models.BooleanField(default = False)
	estadoVentilacion = models.CharField(max_length = 6, default = "")

	def __unicode__(self):
		return "Preferencia: %s, Control: %s, temperatura: %s, estado: %s" % (self.preferencia, self.control, self.temperaturaControl, self.estado)

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
		l.start(self.valor)
		try:
			while nombreHilo['puerto' + str(self.puerto)]:
				pass #para que no se cierre el ciclo hasta que yo diga
				#l.ChangeDutyCycle(self.valor)
				#time.sleep(0.1)
			print "se finalizo el metodo ProcesarDimmer del puerto %s" % self.puerto
		except Exception, e:
			l.stop()
			GPIO.cleanup()
			print "Error en ProcesosLuces/ProcesoRaspberry: %s" % e

#Clase para el sensado de temperatura y humedad
class ProcesosTemperatura():
	def __init__(self, prueba = ""):
		self.prueba = prueba

	def Sensar(self):
		try:
			#el 11 representa que es el DHT11 (si fuera el DHT22 se coloca 22); el 4 representa el numero del puerto
			humedad, temperatura = Adafruit_DHT.read_retry(11, 4) #Sensa la humedad y la temperatura
			
			return humedad, temperatura

		except Exception, e:
			print "Hubo un error en SensarTodo(): \n %s" % e

	def controlManual(self, accion):
		call(['irsend','SEND_ONCE','simply', accion])

	def iniciarProceso(self):
		call(['java', '-jar', 'C:\Users\jfben\OneDrive\Documentos\NetBeansProjects\FuzzyLogicDomo\dist\FuzzyLogicDomo.jar'])