from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from models import *
import json
import threading
import time

#Aqui inicia la pagina principal
def home(request):
	try:
		luz = Luz.objects.all().order_by('puerto')
		lista = [{'nombre':l.nombre, 'puerto':l.puerto, 'valorLuz':l.valorLuz, 'valorDimmer':l.valorDimmer} for l in luz]
		sJsonLuz = json.dumps(lista)
		aire = Aire.objects.get(puerto = 4)
		template = "index.html"
		return render_to_response(template, locals())
	except Exception, e:
		print "Error en Home: %s" % e

#Se usa para cambiar los valores de las preferencias del aire en la base de datos
def preferenciasAire(request, tMinimo, tMaximo, estado):
	try:
		iTempMinima = int(tMinimo)
		iTempMaxima = int(tMaximo)

		aire = Aire.objects.get(puerto = 4)
		aire.temperaturaMinima = iTempMinima
		aire.temperaturaMaxima = iTempMaxima
		aire.estado = estado
		aire.save()

		lista = [{'tMinima':aire.temperaturaMinima, 'tMaxima':aire.temperaturaMaxima, 'valorLuz':aire.estado}]
		sJsonLuz = json.dumps(lista)

		return HttpResponse(sJsonLuz)

	except Exception, e:
		print "Error en preferenciasAire - %s" % e

#Metodo para ejecutar los procesos de encencido, apagado y dimer de las luces
def ProcesoLuz(request, idPuerto, valor, tipo):
	try:
		#Convertir los parametros en numeros
		iPuerto = int(idPuerto)
		iValor	= int(valor)

		#Se consulta el objeto luz que contenga el puerto recibido
		luz = Luz.objects.get(puerto = iPuerto)

		#Si el tipo de cambio lo ejecuta el switch de la luz o el dimer,
		#luego de eso cambia los valores del objeto luz
		if (tipo == "l"):
			luz.valorLuz = iValor
			if (luz.valorLuz == 0):
				luz.valorDimmer = 0
				#se crea objeto de la clase ProcesosLuces con los valores de los parametros
				rpi = ProcesosLuces(iPuerto, iValor, False)

			else:
				luz.valorDimmer = 100
				rpi = ProcesosLuces(iPuerto, iValor)
					
			rpi.ProcesarLuz()
		else:
			rpi = ProcesosLuces(iPuerto, iValor, False)
			time.sleep(0.05)
			luz.valorDimmer = iValor
			if (luz.valorDimmer != 100): 
				rpi = ProcesosLuces(iPuerto, iValor)
			else:
				return ProcesoLuz(iPuerto, 100, 'l')

			hiloDimmer = threading.Thread(target = rpi.ProcesarDimmer, name = 'dimmer' + str(iPuerto))
			hiloDimmer.setDaemon(True)
			hiloDimmer.start()
		#Guarda los cambios en el objeto
		luz.save()

		#El objeto cambiado se formatea en un json para retornar a la pagina
		lista = [{'nombre':luz.nombre, 'puerto':luz.puerto, 'valorLuz':luz.valorLuz, 'valorDimmer':luz.valorDimmer}]
		sJsonLuz = json.dumps(lista)

		return HttpResponse(sJsonLuz)

	except Exception, e:
		print "Error en ProcesoLuz: %s" % e

#Metodo para la ejecucion del sensado de temperatura y humedad
def ejecutarSensor(request):
	rpi = ProcesosTemperatura()

	humedad, temperatura = rpi.SensarTodo()

	temp = [{'humedad':humedad, 'temperatura': temperatura}]
	sJson = json.dumps(temp)

	return HttpResponse(sJson)