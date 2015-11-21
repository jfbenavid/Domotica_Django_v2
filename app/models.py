from django.db import models
import threading
import logging
import time
#import RPi.GPIO as GPIO

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

class ProcesosTemperatura():
	def __init__(self, arg):
 		self.arg = arg

 	#convierte un numero binario que recibe como parametro a decimal
	def BinarioADecimal(sNum):
		return str(int(sNum, 2))

	def sensar():
		data = []
		datos = {}
		bit_count = 0
		tmp = 0
		count = 0
		HumidityBit = ""
		TemperatureBit = ""
		crc = ""

		GPIO.setmode(GPIO.BCM)

		GPIO.setup(4,GPIO.OUT)
		GPIO.output(4,GPIO.HIGH)
		time.sleep(0.025)
		GPIO.output(4,GPIO.LOW)
		time.sleep(0.02)

		GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_UP)

		for i in range(0,500):
		    data.append(GPIO.input(4))

		try:
			while data[count] == 1:
				tmp = 1
				count = count + 1

			for i in range(0, 32):
				bit_count = 0

				while data[count] == 0:
					tmp = 1
					count = count + 1

				while data[count] == 1:
					bit_count = bit_count + 1
					count = count + 1

				if bit_count > 3:
					if i >= 0 and i < 8:
						HumidityBit = HumidityBit + "1"
					if i >= 16 and i < 24:
						TemperatureBit = TemperatureBit + "1"
				else:
					if i >= 0 and i < 8:
						HumidityBit = HumidityBit + "0"
					if i >= 16 and i < 24:
						TemperatureBit = TemperatureBit + "0"

		except:
			print "ERR_RANGE"
			exit(0)

		try:
			for i in range(0, 8):
				bit_count = 0

				while data[count] == 0:
					tmp = 1
					count = count + 1

				while data[count] == 1:
					bit_count = bit_count + 1
					count = count + 1

				if bit_count > 3:
					crc = crc + "1"
				else:
					crc = crc + "0"
		except:
			print "ERR_RANGE"
			exit(0)

		datos['humedad'] = BinarioADecimal(HumidityBit)
		datos['Temperatura'] = BinarioADecimal(TemperatureBit)

		if int(datos['humedad']) + int(datos['Temperatura']) - int(BinarioADecimal(crc)) == 0:
			print "Humidity: " + datos['humedad'] + "%"
			print "Temperature: " + datos['Temperatura'] + "C"
			return datos
		else:
			print "ERR_CRC"

	def SensarTodo():
		try:
			while True:
				datos = sensar()
				#if (datos['humedad']):
				time.sleep(3)
		except Exception, e:
			print "Hubo un error en SensarTodo() - %s" % e