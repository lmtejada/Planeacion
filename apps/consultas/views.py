from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import prefetch_related_objects
from apps.seguimiento.models import FormularioRespuesta, Indicador, Respuesta, Observacion
from apps.login.models import Persona

@login_required()
def listado_view(request):
	title = "Listado de formularios"
	if request.user.groups.filter(name='Administrador').count() == 1:
		extends = 'base/admin_nav.html'
		formulariorespuestas = FormularioRespuesta.objects.filter(enviado=True)
		return render(request, "consultas/form_list_admin.html", {"extends": extends,
																  "title": title,
																  "formulariorespuestas": formulariorespuestas})
	elif request.user.groups.filter(name='Operador').count() == 1:
		extends = 'base/user_nav.html'
		usuario = request.user
		persona = Persona.objects.filter(user=usuario).select_related('entidad').first()
		formulariorespuestas = FormularioRespuesta.objects.filter(entidad=persona.entidad).filter(enviado=True)
		return render(request, "consultas/form_list_user.html", {"extends": extends,
																 "title": title,
																 "formulariorespuestas": formulariorespuestas})

	return redirect('cuenta:home')


@login_required()
def detalle_view(request, pk):
	title = "Detalle"
	if request.user.groups.filter(name='Administrador').count() == 1:
		extends = 'base/admin_nav.html'
	elif request.user.groups.filter(name='Operador').count() == 1:
		extends = 'base/user_nav.html'

	form = FormularioRespuesta.objects.filter(id=int(pk)).prefetch_related('respuesta_set').first()

	if form is not None:
		respuestas = form.respuesta_set.all().order_by('pregunta', 'indicador')
		prefetch_related_objects(respuestas, 'pregunta')
		politicas = []
		indicadores = []
		preguntas = []
		for respuesta in respuestas:
			indicador = Indicador.objects.filter(id=respuesta.indicador.id).select_related('politica_publica').first()
			if indicador not in indicadores:
				indicadores.append(indicador)
			if indicador.politica_publica not in politicas:
				politicas.append(indicador.politica_publica)
			if respuesta.pregunta not in preguntas:
				preguntas.append(respuesta.pregunta)

		if request.method == 'POST':
			if 'estado' in request.POST:
				form.estado = request.POST['estado']
				if request.POST['estado'] == 'no_aprobado':
					form.activo = True
				form.save()
				messages.add_message(request, messages.SUCCESS, 'El formulario ha sido evaluado correctamente.')
			else: 
				if 'observaciones' in request.POST and 'indicador' in request.POST:
					indicador = Indicador.objects.filter(id=request.POST['indicador']).first()
					formObservaciones = Observacion.objects.filter(formulario_respuesta=form).filter(indicador=indicador).first()
					if formObservaciones is None:
						formObservaciones = Observacion(observacion=request.POST['observaciones'], formulario_respuesta=form, indicador=indicador)
						formObservaciones.save()
					else:
						formObservaciones.observacion = request.POST['observaciones']
						formObservaciones.save()
					messages.add_message(request, messages.SUCCESS, 'Su observación ha sido guardada correctamente')
				else:
					messages.add_message(request, messages.ERROR, 'Se ha presentado un error.')
					return render(request, "consultas/detalle.html", {"extends": extends,
															  "title": title,
															  "form": form,
															  "politicas": politicas,
															  "indicadores": indicadores,
															  "preguntas": preguntas,
															  "rol": request.user.groups.filter(name='Administrador').count()})
		
		return render(request, "consultas/detalle.html", {"extends": extends,
														  "title": title,
														  "form": form,
														  "politicas": politicas,
														  "indicadores": indicadores,
														  "preguntas": preguntas,
														  "rol": request.user.groups.filter(name='Administrador').count()})
	else:
		return render(request, "consultas/detalle.html", {"extends": extends,
														"form": 0})

@csrf_exempt
def get_data_view(request):
	if request.method == 'POST':
		indicador = request.POST.get('indicador')
		form_id = request.POST.get('formulario')

		response_data = {}

		formulario = FormularioRespuesta.objects.filter(id=form_id).first()
		respuestas = Respuesta.objects.filter(formulario_respuesta=formulario).filter(indicador__id=indicador)
	
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

		response_data['data'] = {}
		response_data['data']['nivel1'] = {}

		if indicadorInfo1.nivel1 is not None:
			response_data['data']['nivel1']['nombre'] = niveles1[indicadorInfo1.nivel1.nivel]
			response_data['data']['nivel1']['valor'] = indicadorInfo1.nivel1.texto
		else:
			response_data['data']['nivel1']['nombre'] = 'Nivel 1'
			response_data['data']['nivel1']['valor'] = 'No registrado'

		response_data['data']['nivel2'] = {}

		if indicadorInfo2.nivel2 is not None:
			response_data['data']['nivel2']['nombre'] = niveles2[indicadorInfo2.nivel2.nivel]
			response_data['data']['nivel2']['valor'] = indicadorInfo2.nivel2.texto
		else:
			response_data['data']['nivel2']['nombre'] = 'Nivel 2'
			response_data['data']['nivel2']['valor'] = 'No registrado'

		response_data['data']['nivel3'] = {}

		if indicadorInfo2.nivel3 is not None:
			response_data['data']['nivel3']['nombre'] = niveles3[indicadorInfo3.nivel3.nivel]
			response_data['data']['nivel3']['valor'] = indicadorInfo3.nivel3.texto
		else:
			response_data['data']['nivel3']['nombre'] = 'Nivel 3'
			response_data['data']['nivel3']['valor'] = 'No registrado'

		if indicadorInfo1.meta is not None:
			response_data['data']['meta'] = indicadorInfo1.meta
		else:
			response_data['data']['meta'] = 'No registrada'

		if indicadorInfo1.accion is not None:
			response_data['data']['accion'] = indicadorInfo1.accion
		else:
			response_data['data']['accion'] = 'No registrada'

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
			observaciones = Observacion.objects.filter(formulario_respuesta=formulario).filter(indicador=indicadorInfo1).first()
			if observaciones is None:
				response_data['observaciones'] = ''
			else:
				response_data['observaciones'] = observaciones.observacion

		return HttpResponse(
			JsonResponse(response_data)
		)
	else:
		return HttpResponse(
			JsonResponse({"error": "Solicitud no válida."})
		)



	
