from django import forms
from apps.seguimiento.models import FormularioRespuesta, Respuesta

class FormularioRespuestaForm(forms.ModelForm):

	class Meta:
		model = FormularioRespuesta
		fields = [
			'indicador',
		]

class RespuestaForm(forms.ModelForm):

	class Meta:
		model = Respuesta
		fields = [
			'valor',
			'pregunta',
			'formulario_respuesta'
		]