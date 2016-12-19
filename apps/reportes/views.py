from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import prefetch_related_objects
from apps.seguimiento.models import FormularioRespuesta, Indicador, Respuesta, Pregunta, PoliticaPublica, Vigencia
from apps.login.models import Persona

# Create your views here.

@login_required()
def reporte_general_view(request):
	title = "Reporte general"
	politicas = PoliticaPublica.objects.all()
	indicadores = Indicador.objects.all().order_by('id').select_related('politica_publica')

	vigencia = Vigencia.objects.filter(activo=True).select_related('formulario').first()
	headers = Pregunta.objects.filter(formulario=vigencia.formulario).order_by('id')
	formularios = FormularioRespuesta.objects.filter(vigencia=vigencia).prefetch_related('respuesta_set')
	respuestas = {}
	for i in formularios:
		for j in indicadores:
			respuestas[j.id] = i.respuesta_set.filter(indicador=j).order_by('pregunta')
		#respuestas[i.id] = i.respuesta_set.all().order_by('pregunta')
	#prefetch_related_objects(formularios, 'respuesta')
	print(headers)
	print(respuestas)
	
	if request.user.groups.filter(name='Administrador').count() == 1:
		extends = 'base/admin_nav.html'
	elif request.user.groups.filter(name='Operador').count() == 1:
		extends = 'base/user_nav.html'
		
	return render(request, "reportes/general.html", {"extends": extends,
													 "title": title, 
													 "politicas": politicas,
													 "indicadores": indicadores,
													 "headers": headers,
													 "respuestas": respuestas
													 })


def reporte_general2_view(request):	
	if request.user.groups.filter(name='Administrador').count() == 1:
		extends = 'base/admin_nav.html'
	elif request.user.groups.filter(name='Operador').count() == 1:
		extends = 'base/user_nav.html'
		
	return render(request, "reportes/general2.html", {"extends": extends})


def reporte_general3_view(request):	
	if request.user.groups.filter(name='Administrador').count() == 1:
		extends = 'base/admin_nav.html'
	elif request.user.groups.filter(name='Operador').count() == 1:
		extends = 'base/user_nav.html'
		
	return render(request, "reportes/general3.html", {"extends": extends})