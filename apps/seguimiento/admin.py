from django.contrib import admin
from apps.seguimiento.models import Entidad,Persona, PoliticaPublica, Indicador, Formulario, Pregunta

admin.site.register(Entidad)
admin.site.register(Persona)
admin.site.register(PoliticaPublica)
admin.site.register(Indicador)
admin.site.register(Formulario)
admin.site.register(Pregunta)
