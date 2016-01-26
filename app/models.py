from django.db import models
from subprocess import call
import threading
import logging
import time

#lo siguiente es importante para las funcionalidades dentro de la raspberry
import sys
import Adafruit_DHT	#Para el sensado de temperatura
import RPi.GPIO as GPIO	#Para poder utilizar los puertos GPIO

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
	#temperaturaMinima = models.IntegerField(default = 0)
	#temperaturaMaxima = models.IntegerField(default = 0)
	#estado = models.IntegerField(default = 0)

	def __unicode__(self):
		#return "Puerto: %s - Temperatura Maxima: %s - Temperatura Minima: %s - Estado: %s" % (self.puerto, self.temperaturaMaxima, self.temperaturaMinima, self.estado)
		return "Preferencia: %s, Control: %s" % (self.preferencia, self.control)

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
	def __init__(self, prueba = ""):
		self.prueba = prueba

	def Sensar(self):
		try:
			#el 11 representa que es el DHT11 (si fuera el DHT22 se coloca 22); el 4 representa el numero del puerto
			humedad, temperatura = Adafruit_DHT.read_retry(11, 4) #Sensa la humedad y la temperatura
			#aire = Aire.objects.get(puerto = 4) 	#obtiene el objeto con puerto=4 en la base de datos
			#bCambiar = True

			#Si la temperatura esta entre el rango de preferencias apague el puerto 26 de lo contrario prendalo
			# if (temperatura < aire.temperaturaMinima or temperatura > aire.temperaturaMaxima):
			# 	if bCambiar:
			# 		GPIO.setmode(GPIO.BCM)
			# 		GPIO.setup(26, GPIO.OUT) #el puerto 26 es el definido para el aire acondicionado
			# 		GPIO.output(26, True)
			# 		bCambiar = False
			# else:
			# 	GPIO.setmode(GPIO.BCM)
			# 	GPIO.setup(26, GPIO.OUT) #el puerto 26 es el definido para el aire acondicionado
			# 	GPIO.output(26, False)
			# 	bCambiar = True

			return humedad, temperatura

		except Exception, e:
			print "Hubo un error en SensarTodo(): \n %s" % e

	def controlManual(self, accion):
		call(['irsend','SEND_ONCE','hyundai', accion])

	#-----------------------------// Logica Difusa  //----------------------------------

	#Se establece el estado de la humedad como Bajo, Medio o Alto segun el valor capturado por el censor
	def EstablecerHumedad(vHumedad):
		slHumedad = ""
		if(vHumedad < 34):
			slHumedad = "Bajo"
		if(vHumedad > 33 and vHumedad <= 66):
			slHumedad = "Medio"
		if(vHumedad > 66 and vHumedad <= 100):
			slHumedad = "Alto"

		return slHumedad

	#Se establece el estado de la temperatura como Bajo, Medio o Alto segun el valor capturado por el censor
	def EstablecerTemperatura(vTemperatura):
		slTemperatura =""
		if(vTemperatura <= 19):
			slTemperatura = "Bajo"
		if(vTemperatura > 19 and vTemperatura < 24):
			slTemperatura = "Medio"
		if(vTemperatura > 23):
			slTemperatura = "Alto"

		return slTemperatura 

	#Se establece el estado de la preferencia como Bajo, Medio o Alto segun el valor ingresado o seleccionado por el usuario
	def EstablecerPreferencia(vPeferencia):
		slPreferencia =""
		if(vPeferencia == "1"):
			slTemperatura = "Alto"
		if(vPeferencia == "2"):
			slTemperatura = "Medio"
		if(vPeferencia == "3"):
			slTemperatura = "Bajo"

		return slTemperatura

	#Se define el rango de salida de la temperatura y de la humedad
	def ReglaPrincipal(Temperatura, Humedad, Promedio):
		Temperatura_Sal = ""
		Ventilador_Sal  = ""

		if(Temperatura == "Alto" and Humedad == "Alto" and Promedio == "Alto"):
			Temperatura_Sal = "Alto"
			Ventilador_Sal  = "Bajo"

	  	if(Temperatura == "Alto" and Humedad == "Alto" and Promedio == "Medio"):
	  		Temperatura_Sal = "Medio"
	  		Ventilador_Sal  = "Bajo"

	  	if(Temperatura == "Alto" and Humedad == "Alto" and Promedio == "Bajo"):
	  		Temperatura_Sal = "Bajo"
	  		Ventilador_Sal  = "Bajo"

		if(Temperatura == "Alto" and Humedad == "Medio" and Promedio == "Alto"):
			Temperatura_Sal = "Alto"
			Ventilador_Sal  = "Medio"

		if(Temperatura == "Alto" and Humedad == "Medio" and Promedio == "Medio"):
			Temperatura_Sal = "Medio"
			Ventilador_Sal  = "Medio"

		if(Temperatura == "Alto" and Humedad == "Medio" and Promedio == "Bajo"):
			Temperatura_Sal = "Bajo"
			Ventilador_Sal  = "Medio"

		if(Temperatura == "Alto" and Humedad == "Bajo" and Promedio == "Alto"):
			Temperatura_Sal = "Alto"
			Ventilador_Sal  = "Bajo"

		if(Temperatura == "Alto" and Humedad == "Bajo" and Promedio == "Medio"):
			Temperatura_Sal = "Medio"
			Ventilador_Sal  = "Medio"

		if(Temperatura == "Alto " and Humedad == "Bajo" and Promedio == "Bajo"):
			Temperatura_Sal = "Bajo"
			Ventilador_Sal  = "Alto"

		if(Temperatura == "Medio" and Humedad == "Alto" and Promedio == "Alto"):
			Temperatura_Sal = "Alto"
			Ventilador_Sal  = "Bajo"

		if(Temperatura == "Medio" and Humedad == "Alto" and Promedio == "Medio"):
			Temperatura_Sal = "Medio"
			Ventilador_Sal  = "Bajo"

		if(Temperatura == "Medio" and Humedad == "Alto" and Promedio == "Bajo"):
			Temperatura_Sal = "Bajo"
			Ventilador_Sal  = "Bajo"

		if(Temperatura == "Medio" and Humedad == "Medio" and Promedio == "Alto"):
			emperatura_Sal = "Alto"
			Ventilador_Sal = "Medio"

		if(Temperatura == "Medio" and Humedad == "Medio" and Promedio == "Medio"):
			Temperatura_Sal = "Medio"
			Ventilador_Sal  = "Medio"

		if(Temperatura == "Medio" and Humedad == "Medio" and Promedio == "Bajo"):
			Temperatura_Sal = "Bajo"
			Ventilador_Sal  = "Medio"

		if(Temperatura == "Medio" and Humedad == "Bajo" and Promedio == "Alto"):
			Temperatura_Sal = "Alto"
			Ventilador_Sal  = "Bajo"

		if(Temperatura == "Medio" and Humedad == "Bajo" and Promedio == "Medio"):
			Temperatura_Sal = "Medio"
			Ventilador_Sal  = "Medio"

		if(Temperatura == "Medio" and Humedad == "Bajo" and Promedio == "Bajo"):
			Temperatura_Sal = "Bajo"
			Ventilador_Sal  = "Alto"

		if(Temperatura == "Bajo" and Humedad == "Alto" and Promedio == "Alto"):
			Temperatura_Sal = "Alto"
			Ventilador_Sal  = "Bajo"

		if(Temperatura == "Bajo" and Humedad == "Alto" and Promedio == "Medio"):
			Temperatura_Sal = "Medio"
			Ventilador_Sal  = "Medio"

		if(Temperatura == "Bajo" and Humedad == "Alto" and Promedio == "Bajo"):
			Temperatura_Sal = "Bajo"
			Ventilador_Sal  = "Alto"

		if(Temperatura == "Bajo" and Humedad == "Medio" and Promedio == "Alto"):
			Temperatura_Sal = "Alto"
			Ventilador_Sal  = "Medio"

		if(Temperatura == "Bajo" and Humedad == "Medio" and Promedio == "Medio"):
			Temperatura_Sal = "Medio"
			Ventilador_Sal  = "Medio"

		if(Temperatura == "Bajo" and Humedad == "Medio" and Promedio == "Bajo"):
			Temperatura_Sal = "Bajo"
			Ventilador_Sal  = "Medio"

		if(Temperatura == "Bajo" and Humedad == "Bajo" and Promedio == "Alto"):
			Temperatura_Sal = "Alto"
			Ventilador_Sal  = "Bajo"

		if(Temperatura == "Bajo" and Humedad == "Bajo" and Promedio == "Medio"):
			Temperatura_Sal = "Medio"
			Ventilador_Sal  = "Medio"

		if(Temperatura == "Bajo" and Humedad == "Bajo" and Promedio == "Bajo"):
			Temperatura_Sal = "Bajo"
			Ventilador_Sal  = "Alto"

		return (Temperatura_Sal, Ventilador_Sal)

	#Se define la nueva temperatura segun el estado quese procese 
	def ResultadoTemperatura(Temperatura_Salida):
		if Temperatura_Salida == "Bajo":
			return "16"

		if Temperatura_Salida == "Medio":
			return "22"

		if Temperatura_Salida == "Alto":
			return  "26" 

	#Se define la nueva humedad segun el estado quese procese 
	def ResultadoHumedad(Ventilador_Salida):
		if Ventilador_Salida == "Bajo":
			return "3"

		if Ventilador_Salida == "Medio":
			return "2"

		if Ventilador_Salida == "Alto":
			return "1"

	#Fincion que inicia el proceso difuso
	def IniciarProceso(sTemperatura, sHumedad, iPreferencia):
		#sTemperatura = int(input("Ingrese Temperatura"))
		#sHumedad 	 = int(input("Ingrese Humedad"))
		#sPreferencia = str(input("Ingrese Preferencia\n 1 = Alto \n 2 = Medio \n 3 = Bajo"))#muy frio, mas frio, frio , menos frio, poco frio
		if iPreferencia == 1:
			sPreferencia = 'Alto'
		elif iPreferencia == 2:
			sPreferencia = 'Medio'
		elif iPreferencia == 3:
			sPreferencia = 'Bajo'

		#cTemperatura = capturar estado de la Temperatura
		cTemperatura = EstablecerTemperatura(sTemperatura)
		#cHumedad = capturar estado de la humedad
		cHumedad = EstablecerHumedad(sHumedad)
		#cPreferencia = capturar estado de la preferencia del usuario
		cPreferencia = EstablecerPreferencia(sPreferencia)
		if cTemperatura != cPreferencia:
			tuplaResultado = ReglaPrincipal(cTemperatura, cHumedad, cPreferencia)
			resultado_Tem  = ResultadoTemperatura(tuplaResultado[0])
			resultado_Hum  = ResultadoHumedad(tuplaResultado[1])
			
			lista = {'temperatura':resultado_Tem,'humedad':resultado_Hum}
			#return (resultado_Tem, resultado_Hum)
			return lista

		if cTemperatura == cPreferencia:
			return "0"




	#capturarResultado = IniciarProceso()
	#if len(capturarResultado) == 2:
	#	print("La nueva temperatura es: %s y la velocidad %s" %(capturarResultado[0], capturarResultado[1]))
#
	#if capturarResultado == "0":
	#	print("temperatura estable")
	#-----------------------------// Logica Difusa  //----------------------------------