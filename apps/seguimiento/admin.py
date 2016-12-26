from django.contrib import admin
from apps.seguimiento.models import (
	Entidad,
	PoliticaPublica, 
	Indicador,
	Formulario, 
	Pregunta, 
	FormularioRespuesta, 
	Respuesta,
	EjeEstrategico,
	Programa,
	Subprograma,
	Vigencia,
	Nivel1,
	Nivel2, 
	Nivel3)

admin.site.register(Entidad)
admin.site.register(PoliticaPublica)
admin.site.register(Indicador)
admin.site.register(Formulario)
admin.site.register(Pregunta)
admin.site.register(FormularioRespuesta)
admin.site.register(Respuesta)
admin.site.register(EjeEstrategico)
admin.site.register(Programa)
admin.site.register(Subprograma)
admin.site.register(Vigencia)
admin.site.register(Nivel1)
admin.site.register(Nivel2)
admin.site.register(Nivel3)