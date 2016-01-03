# -*- encoding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
#------------------------ para el login y control de logeo
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
##-----------------------
from forms import *
from django.template import RequestContext
from models import *
import json
import threading
import time

#Ejecuta el ingreso del usuario
def home(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/inicio')
	if request.method == 'POST':
		formulario = AuthenticationForm(request.POST)
		if formulario.is_valid:
			usuario = request.POST['username']
			clave = request.POST['password']
			acceso = authenticate(username = usuario, password = clave)
			if acceso is not None:
				if acceso.is_active:
					login(request, acceso)
					return HttpResponseRedirect('/inicio')
				else:
					return render_to_response('noActivo.html', context_instance = RequestContext(request))
			else:
				return render_to_response('noUsuario.html', context_instance = RequestContext(request))
	else:
		formulario = AuthenticationForm()

	return render_to_response("login.html", {'formulario': formulario}, context_instance = RequestContext(request))

#Aqui inicia la pagina principal
@login_required(login_url = '/')
def inicio(request):
	try:
		luz = Luz.objects.all().order_by('puerto')
		lista = [{'nombre':l.nombre, 'puerto':l.puerto, 'valorLuz':l.valorLuz, 'valorDimmer':l.valorDimmer} for l in luz]
		sJsonLuz = json.dumps(lista)
		usuario = request.user
		aire = Aire.objects.get(puerto = 4)
		template = "index.html"
		return render_to_response(template, locals())
	except Exception, e:
		print "Error en Home: %s" % e

#Se usa para cambiar los valores de las preferencias del aire en la base de datos
@login_required(login_url = '/')
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
@login_required(login_url = '/')
def ProcesoLuz(request, idPuerto, valor, tipo):
	try:
		#Convertir los parametros en numeros
		iPuerto = int(idPuerto)
		iValor	= int(valor)

		#Se consulta el objeto luz que contenga el puerto recibido, si no encuentra nada muestra un notfound
		luz = get_object_or_404(Luz.objects.get(puerto = iPuerto))

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
@login_required(login_url = '/')
def ejecutarSensor(request):
	rpi = ProcesosTemperatura()

	humedad, temperatura = rpi.SensarTodo()

	temp = [{'humedad':humedad, 'temperatura': temperatura}]
	sJson = json.dumps(temp)

	return HttpResponse(sJson)

@login_required(login_url = '/')
def cerrar(request):
	logout(request)
	return HttpResponseRedirect('/')

def opciones(request):
	usuario = request.user
	return render_to_response('opciones.html', locals())

@login_required(login_url = '/')
def agregarPuerto(request):
	try:
		usuario = request.user
		if request.method == 'POST':
			form = LuzForm(request.POST)
			if form.is_valid():
				luz = Luz.objects.all()
				existe = False
				for x in luz:
					print 'puertobd = %s recogido = %s' % (x.puerto, request.POST['puerto'])
					if str(x.puerto) == str(request.POST['puerto']):
						existe = True
						break

				if existe:
					print 'el puerto que intenta ingresar ya existe'

				else:
					form.save()
					
				return HttpResponseRedirect('/agregarPuerto')
		else:
			form = LuzForm()

		return render_to_response("opcionesFormulario.html", context_instance = RequestContext(request, {'form':form, 'usuario':usuario}))
	except Exception, e:
		print 'ha ocurrido un error en agregarPuerto()' + str(e)
		raise e
	

@login_required(login_url = '/')
def crearUsuario(request):
	try:
		usuario = request.user
		if request.method == 'POST':
			form = UserCreationForm(request.POST)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/inicio')
		else:
			form = UserCreationForm()

		return render_to_response("opcionesFormulario.html", context_instance = RequestContext(request, {'form':form, 'usuario':usuario}))

	except Exception, e:
		print 'error en la creacion de usuario: %s' % e 
		