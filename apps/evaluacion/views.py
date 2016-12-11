from django.shortcuts import render
from django.contrib import messages
from apps.login.models import Persona
from apps.seguimiento.models import (Entidad, 
									 Indicador, 
									 Formulario, 
									 FormularioRespuesta, 
									 Pregunta, 
									 Respuesta, 
									 PoliticaPublica, 
									 Vigencia, 
									 Proyecto,
									 Subprograma,
									 Programa)
from apps.seguimiento.forms import FormularioRespuestaForm
from django.db.models import prefetch_related_objects, Q
import datetime

def form_view(request):
	title = "Registrar formulario"
	form = FormularioRespuestaForm(request.POST or None)
	respuestas = (request.POST.keys() or None)
	usuario = request.user
	persona = Persona.objects.filter(user=usuario).select_related('entidad').first()
	vigencia = Vigencia.objects.filter(activo=True).select_related('formulario').first()
	if vigencia:
		formulario = Formulario.objects.filter(id=vigencia.formulario.id).prefetch_related('pregunta_set').first()
		preguntas = formulario.pregunta_set.all()
		indicadores = Indicador.objects.filter(entidad=persona.entidad)
		prefetch_related_objects(indicadores, 'politica_publica')
		politicas = []
		for indicador in indicadores:
			if indicador.politica_publica not in politicas:
				politicas.append(indicador.politica_publica)
	else:
		politicas = 0;
		indicadores = 0;
		preguntas = 0;

	if form.is_valid():
		if request.POST['form_id'] == '':
			formularioRespuesta = form.save(commit=False)
			formularioRespuesta.entidad = persona.entidad
			formularioRespuesta.vigencia = vigencia
			if 'enviado' in request.POST:
				formularioRespuesta.activo=False
				if formularioRespuesta.estado is None:
					formularioRespuesta.enviado=True
					formularioRespuesta.fecha_envio=datetime.datetime.now()
			formularioRespuesta.save()
		else:
			formularioRespuesta = FormularioRespuesta.objects.filter(id=request.POST['form_id']).first()
			if 'enviado' in request.POST:
				formularioRespuesta.activo=False
				if formularioRespuesta.estado is None:
					formularioRespuesta.enviado=True
					formularioRespuesta.fecha_envio=datetime.datetime.now()
				formularioRespuesta.save()

		
		if formularioRespuesta is not None:
			for i in respuestas:
				if i.startswith('valor_'):
					valor = request.POST[i]
					if valor != '':
						data = i.split('_', 1)
						respuesta_id = request.POST['respuesta_id_'+data[1]]
						if respuesta_id == '': 
							pregunta = Pregunta.objects.filter(id=data[1]).first()
							respuesta = Respuesta(valor=valor, pregunta=pregunta, formulario_respuesta=formularioRespuesta)
							respuesta.save()
						else:
							respuesta = Respuesta.objects.filter(id=respuesta_id).update(valor=valor)

						if respuesta is None:
							messages.add_message(request, messages.ERROR, 'Se ha presentado un error.')
							break

		else:
			messages.add_message(request, messages.ERROR, 'Se ha presentado un error.')
		
		#return redirect('cuenta:home')
		messages.add_message(request, messages.SUCCESS, 'Sus datos han sido guardado correctamente.')

	return render(request, "seguimiento/formulario.html", {"form": form, 
												   "politicas": politicas,
												   "indicadores": indicadores, 
												   "preguntas": preguntas, 
												   "title": title})
