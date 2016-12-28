from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import prefetch_related_objects, Sum
from django.db import connection
from apps.seguimiento.models import FormularioRespuesta, Indicador, Respuesta, Pregunta, PoliticaPublica, Vigencia, EjeEstrategico, Programa, Subprograma, Nivel1, Nivel2, Nivel3
from apps.login.models import Persona

@login_required()
def reporte_general_view(request):
	title = "Reporte general"
	if request.user.groups.filter(name='Administrador').count() == 1:
		politicas = PoliticaPublica.objects.all()
		indicadores = Indicador.objects.all().order_by('id').select_related('politica_publica')
	elif request.user.groups.filter(name='Operador').count() == 1:
		usuario = request.user
		persona = Persona.objects.filter(user=usuario).select_related('entidad').first()
		indicadores = Indicador.objects.filter(entidad=persona.entidad).order_by('id').select_related('politica_publica')
		politicas = []
		for indicador in indicadores:
			if indicador.politica_publica not in politicas:
				politicas.append(indicador.politica_publica)
	else:
		return redirect('cuenta:home')

	vigencia = Vigencia.objects.filter(activo=True).select_related('formulario').first()
	headers = Pregunta.objects.filter(formulario=vigencia.formulario).order_by('id')
	formularios = FormularioRespuesta.objects.filter(vigencia=vigencia).filter(estado='aprobado').prefetch_related('respuesta_set')
	respuestas = {}

	for i in formularios:
		for j in politicas:
			if i.politica_publica == j:
				respuestas[j.id] = {}
				for k in indicadores:
					respuestas[j.id][k.id] = i.respuesta_set.filter(indicador=k).filter(indicador__politica_publica=j).order_by('pregunta')

	ejes = EjeEstrategico.objects.all()
	programas = Programa.objects.all()
	subprogramas = Subprograma.objects.all()

	
	if request.user.groups.filter(name='Administrador').count() == 1:
		extends = 'base/admin_nav.html'
	elif request.user.groups.filter(name='Operador').count() == 1:
		extends = 'base/user_nav.html'
		
	return render(request, "reportes/general.html", {"extends": extends,
													 "title": title, 
													 "politicas": politicas,
													 "indicadores": indicadores,
													 "headers": headers,
													 "respuestas": respuestas,
													 "ejes": ejes,
													 "programas": programas,
													 "subprogramas": subprogramas
													 })

@login_required()
def reporte_politicas_view(request):
	title = "Reporte por políticas"
	if request.user.groups.filter(name='Administrador').count() == 1:
		politicas = PoliticaPublica.objects.all()
		indicadores = Indicador.objects.all().order_by('id').select_related('politica_publica')
	else:
		return redirect('cuenta:home')

	vigencia = Vigencia.objects.filter(activo=True).select_related('formulario').first()
	preguntas = Pregunta.objects.filter(formulario=vigencia.formulario).order_by('id')
	headers = []
	for i in preguntas:
		if i.id in [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,26, 27, 28, 29, 30, 31, 32, 33, 34, 35,36, 37, 38, 39]:
			headers.append(i)
	
	respuestas = {}

	for i in politicas:
		formulario = FormularioRespuesta.objects.filter(vigencia=vigencia).filter(estado='aprobado').filter(politica_publica=i).prefetch_related('respuesta_set').first()
		if formulario is not None:
			with connection.cursor() as cursor:
				cursor.execute("SELECT seguimiento_respuesta.pregunta_id, SUM(seguimiento_respuesta.valor::INTEGER) AS suma FROM seguimiento_formulariorespuesta INNER JOIN seguimiento_respuesta ON seguimiento_respuesta.formulario_respuesta_id = seguimiento_formulariorespuesta.id WHERE seguimiento_formulariorespuesta.id = %s AND seguimiento_respuesta.pregunta_id IN (9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,26, 27, 28, 29, 30, 31, 32, 33, 34, 35,36, 37, 38, 39) GROUP BY seguimiento_respuesta.pregunta_id order by seguimiento_respuesta.pregunta_id", [formulario.id])
				rows = cursor.fetchall()
				rows = dict(rows)
				respuestas[i.id] = rows
				
	if request.user.groups.filter(name='Administrador').count() == 1:
		extends = 'base/admin_nav.html'
		
	return render(request, "reportes/politicas.html", {"extends": extends,
													 "title": title, 
													 "politicas": politicas,
													 "indicadores": indicadores,
													 "headers": headers,
													 "respuestas": respuestas
													 })

@login_required()
def reporte_nivel1_view(request):
	title = "Reporte general"
	if request.user.groups.filter(name='Administrador').count() == 1:
		politicas = PoliticaPublica.objects.all()
		niveles1 = Nivel1.objects.all().order_by('id')
	else:
		return redirect('cuenta:home')

	vigencia = Vigencia.objects.filter(activo=True).select_related('formulario').first()
	preguntas = Pregunta.objects.filter(formulario=vigencia.formulario).order_by('id')
	headers = []
	for i in preguntas:
		if i.id in [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,26, 27, 28, 29, 30, 31, 32, 33, 34, 35,36, 37, 38, 39]:
			headers.append(i)
	
	respuestas = {}

	for i in politicas:
		formulario = FormularioRespuesta.objects.filter(vigencia=vigencia).filter(estado='aprobado').filter(politica_publica=i).prefetch_related('respuesta_set').first()
		if formulario is not None:
			tmp = formulario.respuesta_set.all()
			prefetch_related_objects(tmp, 'indicador')
			for item in tmp:
				if item.indicador.nivel1 is not None:
					with connection.cursor() as cursor:
						cursor.execute("SELECT seguimiento_pregunta.id, SUM(seguimiento_respuesta.valor::INTEGER) AS sumatoria FROM seguimiento_formulariorespuesta INNER JOIN seguimiento_respuesta ON seguimiento_respuesta.formulario_respuesta_id = seguimiento_formulariorespuesta.id INNER JOIN seguimiento_pregunta ON seguimiento_respuesta.pregunta_id = seguimiento_pregunta.id INNER JOIN seguimiento_indicador ON seguimiento_respuesta.indicador_id = seguimiento_indicador.id INNER JOIN seguimiento_nivel1 ON seguimiento_indicador.nivel1_id = seguimiento_nivel1.id WHERE seguimiento_formulariorespuesta.id = %s AND seguimiento_nivel1.id = %s AND seguimiento_pregunta.id IN (9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,26, 27, 28, 29, 30, 31, 32, 33, 34, 35,36, 37, 38, 39) GROUP BY seguimiento_nivel1.id, seguimiento_pregunta.id order by seguimiento_pregunta.id", [formulario.id, item.indicador.nivel1.id])
						rows = cursor.fetchall()
						rows = dict(rows)
						if rows is not None:
							if formulario.politica_publica.id not in respuestas:
								respuestas[formulario.politica_publica.id] = {}
							respuestas[formulario.politica_publica.id][item.indicador.nivel1.id] = rows

	if request.user.groups.filter(name='Administrador').count() == 1:
		extends = 'base/admin_nav.html'
		
	return render(request, "reportes/nivel.html", {"extends": extends,
													 "title": title, 
													 "politicas": politicas,
													 "niveles": niveles1,
													 "headers": headers,
													 "respuestas": respuestas
													 })