from django import forms
#from django.forms import ModelForm
from models import *

class LuzForm(forms.ModelForm):
	class Meta:
		model = Luz
		exclude = ("valorLuz", "valorDimmer", )