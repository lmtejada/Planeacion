from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView
#from apps.seguimiento.forms import RespuestaForm
from django.core.urlresolvers import reverse_lazy
from apps.login.models import Persona
from apps.seguimiento.models import Entidad, Indicador, Formulario, Pregunta, Respuesta, PoliticaPublica
from apps.seguimiento.forms import FormularioRespuestaForm
from django.db.models import prefetch_related_objects

# Create your views here.

def inicio(request):
	politicas = PoliticaPublica.objects.all()
	entidades = Entidad.objects.all()

	#return HttpResponse("Index")
	return render(request, "seguimiento/index.html", {"entidades": entidades,
													"politicas": politicas})

def form_view(request):
	title = "Registrar formulario"
	form = FormularioRespuestaForm(request.POST or None)
	respuestas = (request.POST.keys() or None)
	usuario = request.user
	persona = Persona.objects.filter(user=usuario).select_related('entidad').first()
	formulario = Formulario.objects.filter(id=1).prefetch_related('pregunta_set').first()
	preguntas = formulario.pregunta_set.all()
	indicadores = Indicador.objects.filter(entidad=persona.entidad)
	prefetch_related_objects(indicadores, 'politica_publica')
	politicas = []
	for indicador in indicadores:
		if indicador.politica_publica not in politicas:
			politicas.append(indicador.politica_publica)

	if form.is_valid():
		formularioRespuesta = form.save(commit=False)
		formularioRespuesta.entidad = persona.entidad
		formularioRespuesta.save()

		for i in respuestas:
			if i.startswith('valor_'):
				valor = request.POST[i]
				if valor != '':
					data = i.split('_', 1)
					pregunta = Pregunta.objects.filter(id=data[1]).first()
					respuesta = Respuesta(valor=valor, pregunta=pregunta, formulario_respuesta=formularioRespuesta)
					respuesta.save()
		
		return redirect('cuenta:home')

	return render(request, "seguimiento/formulario.html", {"form": form, 
												   "politicas": politicas,
												   "indicadores": indicadores, 
												   "preguntas": preguntas, 
												   "title": title})
