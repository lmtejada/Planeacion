from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView
#from apps.seguimiento.forms import RespuestaForm
from django.core.urlresolvers import reverse_lazy
from apps.login.models import Persona
from apps.seguimiento.models import Entidad, Indicador, Pregunta, Respuesta, PoliticaPublica
from apps.seguimiento.forms import FormularioRespuestaForm
from django.http import QueryDict

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
	preguntas = Pregunta.objects.all()
	indicadores = Indicador.objects.all()
	if form.is_valid():
		formularioRespuesta = form.save(commit=False)
		usuario = request.user 
		persona = Persona.objects.filter(user=usuario.id).first()
		entidad = Entidad.objects.filter(nombre=persona.entidad).first()
		formularioRespuesta.entidad = entidad
		formularioRespuesta.save()

		for i in respuestas:
			if i.startswith('valor_'):
				valor = request.POST[i]
				data = i.split('_', 1)
				pregunta = Pregunta.objects.filter(id=data[1]).first()
				respuesta = Respuesta(valor=valor, pregunta=pregunta, formulario_respuesta=formularioRespuesta)
				respuesta.save()

				
		return redirect('seguimiento:index')

	return render(request, "seguimiento/formulario.html", {"form": form, 
												   "indicadores": indicadores, 
												   "preguntas": preguntas, 
												   "title": title})
