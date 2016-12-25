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
									 Programa,
									 Nivel1,
									 Nivel2,
									 Nivel3)

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
			preguntas = formulario.pregunta_set.all().order_by('id')
			indicadores = Indicador.objects.filter(entidad=persona.entidad).order_by('id')
			prefetch_related_objects(indicadores, 'politica_publica')
			politicas = []
			forms = {}
			indicadores_politica = {}
			if len(indicadores) > 0:
				for indicador in indicadores:
					if indicador.politica_publica not in politicas:
						politicas.append(indicador.politica_publica)
						f = FormularioRespuesta.objects.filter(entidad=persona.entidad).filter(vigencia=vigencia).filter(politica_publica=indicador.politica_publica).first()
						if f is not None:
							forms[indicador.politica_publica.id] = f
						else:
							f = FormularioRespuesta(entidad=persona.entidad, vigencia=vigencia, politica_publica=indicador.politica_publica)
							f.save()
							forms[indicador.politica_publica.id] = f

						tmp = PoliticaPublica.objects.filter(id=indicador.politica_publica.id).annotate(num_indicadores=Count('indicador')).first()
						indicadores_politica[indicador.politica_publica.id] = {}
						indicadores_politica[indicador.politica_publica.id]['objeto'] = tmp
						indicadores_politica[indicador.politica_publica.id]['num_enviados'] = 0
						indicadores_politica[indicador.politica_publica.id]['estado'] = 'Incompleto'
						indicadores_politica[indicador.politica_publica.id]['calificacion'] = FormularioRespuesta.objects.filter(politica_publica__id=tmp.id).first()

						resp = Respuesta.objects.filter(formulario_respuesta=f).select_related('indicador').values('indicador').distinct()
						for i in resp:
							politicaTmp = PoliticaPublica.objects.filter(indicador__id=i['indicador']).first() 
							indicadores_politica[politicaTmp.id]['num_enviados'] += 1
							if indicadores_politica[politicaTmp.id]['num_enviados'] == indicadores_politica[politicaTmp.id]['objeto'].num_indicadores:
								indicadores_politica[politicaTmp.id]['estado'] = 'Completo'
							else:
								indicadores_politica[politicaTmp.id]['estado'] = 'Incompleto'

						'''tmp = PoliticaPublica.objects.filter(id=indicador.politica_publica.id).annotate(num_indicadores=Count('indicador')).first()
						tmp2 = FormularioRespuesta.objects.filter(id=forms[indicador.politica_publica.id].id).prefetch_related('respuesta_set').values('respuesta__indicador').distinct().annotate(num_enviados=Count('respuesta__indicador')).first()
						indicadores_politica[indicador.politica_publica.id] = {}
						indicadores_politica[indicador.politica_publica.id]['objeto'] = tmp
						indicadores_politica[indicador.politica_publica.id]['num_enviados'] = 0
						indicadores_politica[indicador.politica_publica.id]['estado'] = 'Incompleto'''
				
				'''tmp = Respuesta.objects.filter(formulario_respuesta=form).select_related('indicador').values('indicador').distinct()
				for i in tmp:
					politicaTmp = PoliticaPublica.objects.filter(indicador__id=i['indicador']).first() 
					indicadores_politica[politicaTmp.id]['num_enviados'] += 1
					if indicadores_politica[politicaTmp.id]['num_enviados'] == indicadores_politica[politicaTmp.id]['objeto'].num_indicadores:
						indicadores_politica[politicaTmp.id]['estado'] = 'Completo'
					else:
						indicadores_politica[politicaTmp.id]['estado'] = 'Incompleto'''
			else:
				indicadores_politica = ''
				politicas = ''
				indicadores = ''
				preguntas = ''
		else:
			politicas = 0
			indicadores = 0
			preguntas = 0
			indicadores_politica = 0
	else:
		politicas = 0
		indicadores = 0
		preguntas = 0 
		indicadores_politica = 0

		if persona.entidad is None:
			politicas = ''
			indicadores = ''
			preguntas = ''
			indicadores_politica = ''

	if request.method == 'POST':
		if 'enviado' in request.POST:
			if 'politica' in request.POST:
				if int(request.POST['politica']) in indicadores_politica:
					if indicadores_politica[int(request.POST['politica'])]['objeto'].num_indicadores != indicadores_politica[int(request.POST['politica'])]['num_enviados']:
						messages.add_message(request, messages.ERROR, 'Para enviar el formulario debe diligenciar la información de todos los indicadores.')
						return render(request, "seguimiento/formulario.html", {"politicas": politicas,
																		   "indicadores": indicadores, 
																		   "preguntas": preguntas, 
																		   "title": title,
																		   "indicadores_politica": indicadores_politica})
				else:
					messages.add_message(request, messages.ERROR, 'Se ha presentado un error.')
					return render(request, "seguimiento/formulario.html", {"politicas": politicas,
																		   "indicadores": indicadores, 
																		   "preguntas": preguntas, 
																		   "title": title,
																		   "indicadores_politica": indicadores_politica})
			else:
				messages.add_message(request, messages.ERROR, 'Se ha presentado un error.')
				return render(request, "seguimiento/formulario.html", {"politicas": politicas,
																	   "indicadores": indicadores, 
																	   "preguntas": preguntas, 
																	   "title": title,
																	   "indicadores_politica": indicadores_politica})

			if int(request.POST['politica']) in forms:
				formRespuesta = forms[int(request.POST['politica'])]
			else:
				messages.add_message(request, messages.ERROR, 'Se ha presentado un error.')
				return render(request, "seguimiento/formulario.html", {"politicas": politicas,
																	   "indicadores": indicadores, 
																	   "preguntas": preguntas, 
																	   "title": title,
																	   "indicadores_politica": indicadores_politica})

			'''for i in indicadores_politica:
				if indicadores_politica[i]['objeto'].num_indicadores != indicadores_politica[i]['num_enviados']:
					messages.add_message(request, messages.ERROR, 'Para enviar el formulario debe diligenciar la información de todos los indicadores.')
					return render(request, "seguimiento/formulario.html", {"politicas": politicas,
																		   "indicadores": indicadores, 
																		   "preguntas": preguntas, 
																		   "title": title,
																	   "indicadores_politica": indicadores_politica})
			'''
			if formRespuesta.activo:
				formRespuesta.activo=False
				if formRespuesta.estado is None:
					formRespuesta.enviado = True
					formRespuesta.fecha_envio = timezone.now()
				formRespuesta.estado = 'pendiente'
				formRespuesta.save()
				messages.add_message(request, messages.SUCCESS, 'Sus datos han sido enviado con éxito.')
			else:
				if formRespuesta.estado == 'aprobado':
					messages.add_message(request, messages.ERROR, 'El formulario ya fue aprobado y no puede ser modificado.')
				elif formRespuesta.estado == 'pendiente':
					messages.add_message(request, messages.ERROR, 'El formulario se encuentra en proceso de revisión y no puede ser modificado.')
	
		else:
			if 'politica' in request.POST:
				if int(request.POST['politica']) in forms:
					formRespuesta = forms[int(request.POST['politica'])]
				else:
					messages.add_message(request, messages.ERROR, 'Se ha presentado un error.')
					return render(request, "seguimiento/formulario.html", {"politicas": politicas,
																		   "indicadores": indicadores, 
																		   "preguntas": preguntas, 
																		   "title": title,
																		   "indicadores_politica": indicadores_politica})
			else:
				messages.add_message(request, messages.ERROR, 'Se ha presentado un error.')
				return render(request, "seguimiento/formulario.html", {"politicas": politicas,
																	   "indicadores": indicadores, 
																	   "preguntas": preguntas, 
																	   "title": title,
																	   "indicadores_politica": indicadores_politica})
			if formRespuesta is not None:
				if 'indicador' in request.POST:
					indicador = Indicador.objects.filter(id=request.POST['indicador']).first()
					if indicador is None:
						messages.add_message(request, messages.ERROR, 'Se ha presentado un error.')
						return render(request, "seguimiento/formulario.html", {"politicas": politicas,
																			   "indicadores": indicadores, 
																			   "preguntas": preguntas, 
																			   "title": title,
																			   "indicadores_politica": indicadores_politica})
				else: 
					messages.add_message(request, messages.ERROR, 'Se ha presentado un error.')
					return render(request, "seguimiento/formulario.html", {"politicas": politicas,
																		   "indicadores": indicadores, 
																		   "preguntas": preguntas, 
																		   "title": title,
																		   "indicadores_politica": indicadores_politica})
				
				for i in respuestas:
					if i.startswith('valor_'):
						valor = request.POST[i]
						if valor != '':
							data = i.split('_', 1)
							if 'respuesta_id_'+data[1] in request.POST:
								respuesta_id = request.POST['respuesta_id_'+data[1]]
							else:
								messages.add_message(request, messages.ERROR, 'Se ha presentado un error.')
								return render(request, "seguimiento/formulario.html", {"politicas": politicas,
																					   "indicadores": indicadores, 
																					   "preguntas": preguntas, 
																					   "title": title,
																					   "indicadores_politica": indicadores_politica})
							if respuesta_id == '': 
								pregunta = Pregunta.objects.filter(id=data[1]).first()
								respuesta = Respuesta(valor=valor, pregunta=pregunta, indicador=indicador, formulario_respuesta=formRespuesta)
								respuesta.save()
							else:
								respuesta = Respuesta.objects.filter(id=respuesta_id).update(valor=valor)

							if respuesta is None:
								messages.add_message(request, messages.ERROR, 'Se ha presentado un error.')
								return render(request, "seguimiento/formulario.html", {"politicas": politicas,
																					   "indicadores": indicadores, 
																					   "preguntas": preguntas, 
																					   "title": title,
																					   "indicadores_politica": indicadores_politica})

				resp = Respuesta.objects.filter(formulario_respuesta=formRespuesta).select_related('indicador').values('indicador').distinct()
				for i in resp:
					politicaTmp = PoliticaPublica.objects.filter(indicador__id=i['indicador']).first() 
					indicadores_politica[politicaTmp.id]['num_enviados'] = 0
				for i in resp:
					politicaTmp = PoliticaPublica.objects.filter(indicador__id=i['indicador']).first() 
					indicadores_politica[politicaTmp.id]['num_enviados'] += 1
					if indicadores_politica[politicaTmp.id]['num_enviados'] == indicadores_politica[politicaTmp.id]['objeto'].num_indicadores:
						indicadores_politica[politicaTmp.id]['estado'] = 'Completo'
					else:
						indicadores_politica[politicaTmp.id]['estado'] = 'Incompleto'

				messages.add_message(request, messages.SUCCESS, 'Sus datos han sido guardado correctamente.')

			else:
				messages.add_message(request, messages.ERROR, 'Se ha presentado un error.')
				return render(request, "seguimiento/formulario.html", {"politicas": politicas,
																	   "indicadores": indicadores, 
																	   "preguntas": preguntas, 
																	   "title": title,
																	   "indicadores_politica": indicadores_politica})

	return render(request, "seguimiento/formulario.html", {"politicas": politicas,
												   			"indicadores": indicadores, 
												   			"preguntas": preguntas, 
												  			"title": title,
												   			"indicadores_politica": indicadores_politica})

@csrf_exempt
def get_data_view(request):
	if request.method == 'POST':
		indicador = request.POST.get('indicador')
		politica = request.POST.get('politica')

		response_data = {}

		vigencia = Vigencia.objects.filter(activo=True)
		usuario = request.user
		persona = Persona.objects.filter(user=usuario).select_related('entidad').first()
		formulario = FormularioRespuesta.objects.filter(entidad=persona.entidad).filter(vigencia=vigencia).filter(politica_publica__id=politica).first()
		respuestas = Respuesta.objects.filter(formulario_respuesta=formulario).filter(indicador__id=indicador)
		indicadorInfo = Indicador.objects.filter(id=indicador).select_related('proyecto').first()
		proyecto = Proyecto.objects.filter(id=indicadorInfo.proyecto.id).select_related('subprograma').first()
		subprograma = Subprograma.objects.filter(id=proyecto.subprograma.id).select_related('programa').first()
		programa = Programa.objects.filter(id=subprograma.programa.id).select_related('eje_estrategico').first()

		response_data['data'] = {}
		response_data['data']['proyecto'] = proyecto.codigo+' - '+proyecto.nombre
		response_data['data']['subprograma'] = subprograma.codigo+' - '+subprograma.nombre
		response_data['data']['programa'] = programa.codigo+' - '+programa.nombre
		response_data['data']['eje_estrategico'] = programa.eje_estrategico.codigo+' - '+programa.eje_estrategico.nombre
		
		indicadorInfo1 = Indicador.objects.filter(id=indicador).select_related('nivel1').first()
		indicadorInfo2 = Indicador.objects.filter(id=indicador).select_related('nivel2').first()
		indicadorInfo3 = Indicador.objects.filter(id=indicador).select_related('nivel3').first()
		
		niveles1 = {
	        '1':'Línea orientadora',
			'2':'Línea estratégica',
			'3':'Categoría',
			'4':'Objetivo estratégico',
			'5':'Estrategia',
			'6':'Objetivo de la política',
		}

		niveles2 = {
		    '1': 'Categoría de la política',
		    '2': 'Estrategia',
		    '3': 'Objetivo de la política',
		    '4': 'Acciones recomendadas',
		}

		niveles3 = {
		    '1': 'Objetivo de la política',
		    '2': 'Acciones recomendadas',
		    '3': 'Estrategia',
		}

		response_data['data']['nivel1'] = {}
		response_data['data']['nivel1']['nombre'] = niveles1[indicadorInfo1.nivel1.nivel]
		response_data['data']['nivel1']['valor'] = indicadorInfo1.nivel1.texto

		response_data['data']['nivel2'] = {}
		response_data['data']['nivel2']['nombre'] = niveles2[indicadorInfo2.nivel2.nivel]
		response_data['data']['nivel2']['valor'] = indicadorInfo2.nivel2.texto

		response_data['data']['nivel3'] = {}
		response_data['data']['nivel3']['nombre'] = niveles3[indicadorInfo3.nivel3.nivel]
		response_data['data']['nivel3']['valor'] = indicadorInfo3.nivel3.texto

		if formulario is not None:
			prefetch_related_objects(respuestas, 'pregunta')
			response_data['estado'] = formulario.estado
			response_data['activo'] = formulario.activo
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
