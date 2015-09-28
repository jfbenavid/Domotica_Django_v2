from django.db import models
import RPi.GPIO as GPIO

class Luz(models.Model):
	puerto = models.IntegerField(default = 0)
	valorLuz = models.IntegerField(default = 0)
	valorDimmer = models.IntegerField(default = 0)
	
	def __unicode__(self):
		return "%s - %s - %s" % (self.puerto, self.valorLuz, self.valorDimmer)

class ProcesosLuces():
	def __init__(self, id_puerto, valor):
		self.puerto = id_puerto
		self.valor = valor

	def ProcesoRaspberry(self):
		print "Aqui es Models.py este es el puerto: %s y el valor es este %s" % (self.puerto, self.valor)
		#aqui se hace el proceso de la luz en el puerto de la raspberry
		try:
			GPIO.setmode(GPIO.BCM)
			GPIO.setup(self.puerto, GPIO.OUT)
			luz = GPIO.PWM(self.puerto, self.valor)
			luz.start(0)
			while True:
				luz.ChangeDutyCycle(self.valor)
		except Exception, e:
			luz.stop()
			GPIO.cleanup()
			print "Error en ProcesosLuces/ProcesoRaspberry: %s" % e