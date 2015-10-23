from django.db import models
import RPi.GPIO as GPIO
import time

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
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.puerto, GPIO.OUT)
		bOnOff = False

		if (self.valor == 1):
			bOnOff = True

		GPIO.output(self.puerto, bOnOff)

	def ProcesarDimmer(self):
		print "Aqui es Models.py este es el puerto: %s y el valor es este %s" % (self.puerto, self.valor)
		#aqui se hace el proceso de la luz en el puerto de la raspberry
	#	GPIO.setmode(GPIO.BCM)
	#	GPIO.setup(self.puerto, GPIO.OUT)
	#	l = GPIO.PWM(self.puerto, 100)
	#	l.start(100)
		#try:
		#	while True:
		#		l.ChangeDutyCycle(self.valor)
		#		time.sleep(0.1)
		#	print "aqui se ejecuto todo bien en el metodo ProcesarDimmer .l."
		#except Exception, e:
		#	luz.stop()
		#	GPIO.cleanup()
		#	print "Error en ProcesosLuces/ProcesoRaspberry: %s" % e