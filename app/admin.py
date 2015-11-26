#Para la muestra de las entidades de la base de datos en la pagina del admin

from django.contrib import admin
from models import *

admin.site.register(Luz)
admin.site.register(Aire)