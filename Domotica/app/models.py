from django.db import models

class Luz(models.Model):
	puerto = models.IntegerField(default = 0)
	valorLuz = models.IntegerField(default = 0)
	valorDimmer = models.IntegerField(default = 0)
	
	def __unicode__(self):
		return "%s - %s - %s" % (self.puerto, self.valorLuz, self.valorDimmer)
