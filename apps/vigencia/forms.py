from django import forms
from apps.seguimiento.models import Vigencia

class VigenciaForm(forms.ModelForm):
	class Meta:
		model = Vigencia
		fields = [
			'fecha_inicio',
			'fecha_fin',
			'formulario'
		]