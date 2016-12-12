from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import prefetch_related_objects, Q, Count
from django.utils import timezone
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


def inicio(request):
	politicas = PoliticaPublica.objects.all()
	entidades = Entidad.objects.all()
	return render(request, "seguimiento/index.html", {"entidades": entidades,
													  "politicas": politicas})

def form_view(request):
	title = "Registrar formulario"
	respuestas = (request.POST.keys() or None)
	usuario = request.user
	persona = Persona.objects.filter(user=usuario).select_related('entidad').first()
	fecha_actual = timezone.now()
	vigencia = Vigencia.objects.filter(activo=True).select_related('formulario').first()
	if vigencia and persona.entidad is not None:
		if fecha_actual >= vigencia.fecha_inicio and fecha_actual <= vigencia.fecha_fin:
			formulario = Formulario.objects.filter(id=vigencia.formulario.id).prefetch_related('pregunta_set').first()
			preguntas = formulario.pregunta_set.all()
			indicadores = Indicador.objects.filter(entidad=persona.entidad)
			prefetch_related_objects(indicadores, 'politica_publica')
			politicas = []
			indicadores_politica = {}
			if len(indicadores) > 0:
				for indicador in indicadores:
					if indicador.politica_publica not in politicas:
						politicas.append(indicador.politica_publica)
						tmp = PoliticaPublica.objects.filter(id=indicador.politica_publica.id).annotate(num_indicadores=Count('indicador')).first()
						indicadores_politica[indicador.politica_publica.id] = {}
						indicadores_politica[indicador.politica_publica.id]['objeto'] = tmp
						indicadores_politica[indicador.politica_publica.id]['num_enviados'] = 0
						indicadores_politica[indicador.politica_publica.id]['estado'] = 'Incompleto'

				form = FormularioRespuesta.objects.filter(entidad=persona.entidad).filter(vigencia=vigencia).first()
				if form is None:
					form = FormularioRespuesta(entidad=persona.entidad, vigencia=vigencia)
					form.save()
				else:
					tmp = Respuesta.objects.filter(formulario_respuesta=form).select_related('indicador').values('indicador').distinct()
					for i in tmp:
						politicaTmp = PoliticaPublica.objects.filter(indicador__id=i['indicador']).first() 
						indicadores_politica[politicaTmp.id]['num_enviados'] += 1
						if indicadores_politica[politicaTmp.id]['num_enviados'] == indicadores_politica[politicaTmp.id]['objeto'].num_indicadores:
							indicadores_politica[politicaTmp.id]['estado'] = 'Completo'
						else:
							indicadores_politica[politicaTmp.id]['estado'] = 'Incompleto'
			else:
				indicadores_politica = 0;
				politicas = '';
				indicadores = '';
				preguntas = '';

		else:
			politicas = 0;
			indicadores = 0;
			preguntas = 0;
	else:
		politicas = 0;
		indicadores = 0;
		preguntas = 0; 

		if persona.entidad is None:
			politicas = '';
			indicadores = '';
			preguntas = '';

	if request.method == 'POST':
		if 'enviado' in request.POST:
			for i in indicadores_politica:
				if indicadores_politica[i]['objeto'].num_indicadores != indicadores_politica[i]['num_enviados']:
					messages.add_message(request, messages.ERROR, 'Para enviar el formulario debe diligenciar la información de todos los indicadores.')
					return render(request, "seguimiento/formulario.html", {"form": form, 
																		   "politicas": politicas,
																		   "indicadores": indicadores, 
																		   "preguntas": preguntas, 
																		   "title": title,
																		   "indicadores_politica": indicadores_politica})
			if form.activo:
				form.activo=False
				if form.estado is None:
					form.enviado = True
					form.fecha_envio = timezone.now()
					form.estado = 'pendiente'
				form.save()
				messages.add_message(request, messages.SUCCESS, 'Sus datos han sido enviado con éxito.')
			else:
				if form.estado == 'aprobado':
					messages.add_message(request, messages.ERROR, 'El formulario ya fue aprobado y no puede ser modificado.')
				elif form.estado == 'pendiente':
					messages.add_message(request, messages.ERROR, 'El formulario se encuentra en proceso de revisión y no puede ser modificado.')
		else:
			if form is not None:
				for i in respuestas:
					if i.startswith('valor_'):
						valor = request.POST[i]
						if valor != '':
							data = i.split('_', 1)
							respuesta_id = request.POST['respuesta_id_'+data[1]]
							if respuesta_id == '': 
								pregunta = Pregunta.objects.filter(id=data[1]).first()
								if request.POST['indicador']:
									indicador = Indicador.objects.filter(id=request.POST['indicador']).first()
								else: 
									messages.add_message(request, messages.ERROR, 'Se ha presentado un error.')
									return render(request, "seguimiento/formulario.html", {"form": form, 
																						   "politicas": politicas,
																					   	   "indicadores": indicadores, 
																					       "preguntas": preguntas, 
																					       "title": title,
																					      "indicadores_politica": indicadores_politica})
								respuesta = Respuesta(valor=valor, pregunta=pregunta, indicador=indicador, formulario_respuesta=form)
								respuesta.save()
							else:
								respuesta = Respuesta.objects.filter(id=respuesta_id).update(valor=valor)

							if respuesta is None:
								messages.add_message(request, messages.ERROR, 'Se ha presentado un error.')
								return render(request, "seguimiento/formulario.html", {"form": form, 
																					   "politicas": politicas,
																					   "indicadores": indicadores, 
																					   "preguntas": preguntas, 
																					   "title": title,
																					   "indicadores_politica": indicadores_politica})

				indicador = Indicador.objects.filter(id=request.POST['indicador']).first()
				politicaTmp = PoliticaPublica.objects.filter(indicador__id=indicador.id).first()
				indicadores_politica[politicaTmp.id]['num_enviados'] += 1
				if indicadores_politica[politicaTmp.id]['num_enviados'] == indicadores_politica[politicaTmp.id]['objeto'].num_indicadores:
					indicadores_politica[indicador.politica_publica.id]['estado'] = 'Completo'
				else:
					indicadores_politica[indicador.politica_publica.id]['estado'] = 'Incompleto'
				messages.add_message(request, messages.SUCCESS, 'Sus datos han sido guardado correctamente.')

			else:
				messages.add_message(request, messages.ERROR, 'Se ha presentado un error.')
				return render(request, "seguimiento/formulario.html", {"form": form, 
																	   "politicas": politicas,
																	   "indicadores": indicadores, 
																	   "preguntas": preguntas, 
																	   "title": title,
																	   "indicadores_politica": indicadores_politica})

	return render(request, "seguimiento/formulario.html", {"form": form, 
												   "politicas": politicas,
												   "indicadores": indicadores, 
												   "preguntas": preguntas, 
												   "title": title,
												   "indicadores_politica": indicadores_politica})

@csrf_exempt
def get_data_view(request):
	if request.method == 'POST':
		indicador = request.POST.get('indicador')
		response_data = {}

		vigencia = Vigencia.objects.filter(activo=True)
		usuario = request.user
		persona = Persona.objects.filter(user=usuario).select_related('entidad').first()
		formulario = FormularioRespuesta.objects.filter(entidad=persona.entidad).filter(vigencia=vigencia).first()
		respuestas = Respuesta.objects.filter(formulario_respuesta=formulario).filter(indicador__id=indicador)
		#formulario = FormularioRespuesta.objects.filter(indicador__id=indicador).filter(vigencia=vigencia).prefetch_related('respuesta_set').first()
		indicadorInfo = Indicador.objects.filter(id=indicador).select_related('proyecto').first()
		proyecto = Proyecto.objects.filter(id=indicadorInfo.proyecto.id).select_related('subprograma').first()
		subprograma = Subprograma.objects.filter(id=proyecto.subprograma.id).select_related('programa').first()
		programa = Programa.objects.filter(id=subprograma.programa.id).select_related('eje_estrategico').first()

		response_data['data'] = {}
		response_data['data']['proyecto'] = proyecto.codigo+' - '+proyecto.nombre
		response_data['data']['subprograma'] = subprograma.codigo+' - '+subprograma.nombre
		response_data['data']['programa'] = programa.codigo+' - '+programa.nombre
		response_data['data']['eje_estrategico'] = programa.eje_estrategico.codigo+' - '+programa.eje_estrategico.nombre

		if formulario is not None:
			#respuestas = formulario.respuesta_set.all()
			prefetch_related_objects(respuestas, 'pregunta')
			response_data['estado'] = formulario.estado
			response_data['activo'] = formulario.activo
			#response_data['form_id'] = formulario.id
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
