from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import prefetch_related_objects
from apps.seguimiento.models import FormularioRespuesta, Indicador
from apps.login.models import Persona

@login_required()
def listado_view(request):

	if request.user.groups.filter(name='Administrador').count() == 1:
		extends = 'base/admin_nav.html'
		formulariorespuestas = FormularioRespuesta.objects.filter(enviado=True)
		return render(request, "consultas/form_list_admin.html", {"extends": extends,
																"formulariorespuestas": formulariorespuestas})
	elif request.user.groups.filter(name='Operador').count() == 1:
		extends = 'base/user_nav.html'
		usuario = request.user
		persona = Persona.objects.filter(user=usuario).select_related('entidad').first()
		formulariorespuestas = FormularioRespuesta.objects.filter(entidad=persona.entidad).filter(enviado=True)
		return render(request, "consultas/form_list_user.html", {"extends": extends,
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
			if request.POST['estado']:
				form.estado = request.POST['estado']
				if request.POST['estado'] == 'no_aprobado':
					form.activo = True
			else: 
				messages.add_message(request, messages.ERROR, 'Se ha presentado un error.')
				return render(request, "consultas/detalle.html", {"extends": extends,
														  "title": title,
														  "form": form,
														  "politicas": politicas,
														  "indicadores": indicadores,
														  "preguntas": preguntas,
														  "rol": request.user.groups.filter(name='Administrador').count()})

			if 'observaciones' in request.POST:
				form.observaciones = request.POST['observaciones']

			form.save()
			messages.add_message(request, messages.SUCCESS, 'El formulario ha sido evaluado correctamente.')
		
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




	
