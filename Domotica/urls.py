"""Domotica URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
	#Pagina inicial 'Login'
	url(r'^$', 'app.views.home', name = 'home'),
	#Pagina principal: index
	url(r'^inicio/$', 'app.views.inicio', name = 'inicio'),
	#Se deben pasar 3 valores (2 numericos y una letra entre l y d)
	url(r'^ProcesoLuz/(\d+) (\d+) (l|d)/$', 'app.views.ProcesoLuz', name = 'ProcesoLuz'),
	#Se deben pasar 3 numeros a las preferencias del aire para poder ejecutarlo correctamente
	url(r'^preferenciasAire/(\d+) (\d+) (\d)/$', 'app.views.preferenciasAire', name = 'preferenciasAire'),
	#Pagina que ejecuta los procesos del sensor
	url(r'^ejecutarSensor/$', 'app.views.ejecutarSensor', name = 'ejecutarSensor'),
	#Url para cerrar la sesion activa
	url(r'^cerrar/$', 'app.views.cerrar', name = 'cerrar'),
	#Pagina con formulario para agregar nuevo puerto
	url(r'^opciones/$', 'app.views.opciones', name = 'opciones'),
	url(r'^opciones/agregarPuerto/$', 'app.views.agregarPuerto', name = 'agregarPuerto'),
	url(r'^opciones/crearUsuario/$', 'app.views.crearUsuario', name = 'crearUsuario'),
]
