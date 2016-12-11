from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
#from apps.seguimiento.forms import RespuestaForm
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
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


def inicio(request):
	politicas = PoliticaPublica.objects.all()
	entidades = Entidad.objects.all()
	return render(request, "seguimiento/index.html", {"entidades": entidades,
													"politicas": politicas})

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

@csrf_exempt
def get_data_view(request):
	if request.method == 'POST':
		indicador = request.POST.get('indicador')
		response_data = {}

		vigencia = Vigencia.objects.filter(activo=True)
		formulario = FormularioRespuesta.objects.filter(indicador__id=indicador).filter(vigencia=vigencia).prefetch_related('respuesta_set').first()
		indicadorInfo = Indicador.objects.filter(id=indicador).select_related('proyecto').first()
		proyecto = Proyecto.objects.filter(id=indicadorInfo.proyecto.id).select_related('subprograma').first()
		subprograma = Subprograma.objects.filter(id=proyecto.subprograma.id).select_related('programa').first()
		programa = Programa.objects.filter(id=subprograma.programa.id).select_related('eje_estrategico').first()

		response_data['data'] = {}
		response_data['data']['proyecto'] = proyecto.codigo+' - '+proyecto.nombre
		response_data['data']['subprograma'] = subprograma.codigo+' - '+subprograma.nombre
		response_data['data']['programa'] = programa.codigo+' - '+programa.nombre
		response_data['data']['eje_estrategico'] = programa.eje_estrategico.codigo+' - '+programa.eje_estrategico.nombre

		print(programa.eje_estrategico.id)
		if formulario is not None:
			respuestas = formulario.respuesta_set.all()
			prefetch_related_objects(respuestas, 'pregunta')
			if formulario.estado is None:
				response_data['estado'] = False
			else:
				response_data['estado'] = formulario.estado
			response_data['activo'] = formulario.activo
			response_data['form_id'] = formulario.id
			response_data['respuestas'] = {}
			for i in respuestas:
				temp = {}
				temp['pregunta_id'] = i.pregunta.id
				temp['respuesta_id'] = i.id
				temp['valor'] = i.valor
				response_data['respuestas'][i.pregunta.id] = temp

		return HttpResponse(
			JsonResponse(response_data)
		)
	else:
		return HttpResponse(
			JsonResponse({"error": "Solicitud no válida."})
		)
