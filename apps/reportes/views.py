from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import prefetch_related_objects, Sum
from django.db import connection
from apps.seguimiento.models import IndicadorEntidad, FormularioRespuesta, Indicador, Respuesta, Pregunta, PoliticaPublica, Vigencia, EjeEstrategico, Programa, Subprograma, Nivel1, Nivel2, Nivel3
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




@login_required()
def reporte_nivel2_view(request):
	title = "Reporte general"
	if request.user.groups.filter(name='Administrador').count() == 1:
		politicas = PoliticaPublica.objects.all()
		niveles2 = Nivel2.objects.all().order_by('id')
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
				if item.indicador.nivel2 is not None:
					with connection.cursor() as cursor:
						cursor.execute("SELECT seguimiento_pregunta.id, SUM(seguimiento_respuesta.valor::INTEGER) AS sumatoria FROM seguimiento_formulariorespuesta INNER JOIN seguimiento_respuesta ON seguimiento_respuesta.formulario_respuesta_id = seguimiento_formulariorespuesta.id INNER JOIN seguimiento_pregunta ON seguimiento_respuesta.pregunta_id = seguimiento_pregunta.id INNER JOIN seguimiento_indicador ON seguimiento_respuesta.indicador_id = seguimiento_indicador.id INNER JOIN seguimiento_nivel2 ON seguimiento_indicador.nivel2_id = seguimiento_nivel2.id WHERE seguimiento_formulariorespuesta.id = %s AND seguimiento_nivel2.id = %s AND seguimiento_pregunta.id IN (9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,26, 27, 28, 29, 30, 31, 32, 33, 34, 35,36, 37, 38, 39) GROUP BY seguimiento_nivel2.id, seguimiento_pregunta.id order by seguimiento_pregunta.id", [formulario.id, item.indicador.nivel2.id])
						rows = cursor.fetchall()
						rows = dict(rows)
						if rows is not None:
							if formulario.politica_publica.id not in respuestas:
								respuestas[formulario.politica_publica.id] = {}
							respuestas[formulario.politica_publica.id][item.indicador.nivel2.id] = rows

	if request.user.groups.filter(name='Administrador').count() == 1:
		extends = 'base/admin_nav.html'
		
	return render(request, "reportes/nivel.html", {"extends": extends,
													 "title": title, 
													 "politicas": politicas,
													 "niveles": niveles2,
													 "headers": headers,
													 "respuestas": respuestas
													 })



@login_required()
def reporte_nivel3_view(request):
	title = "Reporte general"
	if request.user.groups.filter(name='Administrador').count() == 1:
		politicas = PoliticaPublica.objects.all()
		niveles3 = Nivel3.objects.all().order_by('id')
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
				if item.indicador.nivel2 is not None:
					with connection.cursor() as cursor:
						cursor.execute("SELECT seguimiento_pregunta.id, SUM(seguimiento_respuesta.valor::INTEGER) AS sumatoria FROM seguimiento_formulariorespuesta INNER JOIN seguimiento_respuesta ON seguimiento_respuesta.formulario_respuesta_id = seguimiento_formulariorespuesta.id INNER JOIN seguimiento_pregunta ON seguimiento_respuesta.pregunta_id = seguimiento_pregunta.id INNER JOIN seguimiento_indicador ON seguimiento_respuesta.indicador_id = seguimiento_indicador.id INNER JOIN seguimiento_nivel3 ON seguimiento_indicador.nivel3_id = seguimiento_nivel3.id WHERE seguimiento_formulariorespuesta.id = %s AND seguimiento_nivel3.id = %s AND seguimiento_pregunta.id IN (9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,26, 27, 28, 29, 30, 31, 32, 33, 34, 35,36, 37, 38, 39) GROUP BY seguimiento_nivel3.id, seguimiento_pregunta.id order by seguimiento_pregunta.id", [formulario.id, item.indicador.nivel3.id])
						rows = cursor.fetchall()
						rows = dict(rows)
						if rows is not None:
							if formulario.politica_publica.id not in respuestas:
								respuestas[formulario.politica_publica.id] = {}
							respuestas[formulario.politica_publica.id][item.indicador.nivel3.id] = rows

	if request.user.groups.filter(name='Administrador').count() == 1:
		extends = 'base/admin_nav.html'
		
	return render(request, "reportes/nivel.html", {"extends": extends,
													 "title": title, 
													 "politicas": politicas,
													 "niveles": niveles3,
													 "headers": headers,
													 "respuestas": respuestas
													 })


@login_required()
def reporte_eje_view(request):
	title = "Reporte general"
	if request.user.groups.filter(name='Administrador').count() == 1:
		politicas = PoliticaPublica.objects.all()
		ejes = EjeEstrategico.objects.all().order_by('id')
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
				relacion = IndicadorEntidad.objects.filter(indicador__id=item.indicador.id).select_related('subprograma').first() 
				if relacion.subprograma is not None:
					programa = Programa.objects.filter(id=relacion.subprograma.programa_id).select_related('eje_estrategico').first()
					if programa is not None:
						if programa.eje_estrategico is not None:
							with connection.cursor() as cursor:
								cursor.execute("SELECT seguimiento_pregunta.id, SUM(seguimiento_respuesta.valor::INTEGER) AS sumatoria FROM seguimiento_formulariorespuesta INNER JOIN seguimiento_respuesta ON seguimiento_respuesta.formulario_respuesta_id = seguimiento_formulariorespuesta.id INNER JOIN seguimiento_pregunta ON seguimiento_respuesta.pregunta_id = seguimiento_pregunta.id INNER JOIN seguimiento_indicador ON seguimiento_respuesta.indicador_id = seguimiento_indicador.id INNER JOIN seguimiento_indicadorentidad ON seguimiento_indicadorentidad.indicador_id = seguimiento_indicador.id INNER JOIN seguimiento_subprograma ON seguimiento_indicadorentidad.subprograma_id = seguimiento_subprograma.id INNER JOIN seguimiento_programa ON seguimiento_subprograma.programa_id = seguimiento_programa.id INNER JOIN seguimiento_ejeestrategico ON seguimiento_programa.eje_estrategico_id = seguimiento_ejeestrategico.id WHERE seguimiento_formulariorespuesta.id = %s AND seguimiento_ejeestrategico.id = %s AND seguimiento_pregunta.id IN (9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,26, 27, 28, 29, 30, 31, 32, 33, 34, 35,36, 37, 38, 39) GROUP BY seguimiento_ejeestrategico.id, seguimiento_pregunta.id order by seguimiento_pregunta.id", [formulario.id, programa.eje_estrategico.id])
								rows = cursor.fetchall()
								rows = dict(rows)
								if rows is not None:
									if formulario.politica_publica.id not in respuestas:
										respuestas[formulario.politica_publica.id] = {}
									respuestas[formulario.politica_publica.id][programa.eje_estrategico.id] = rows

	if request.user.groups.filter(name='Administrador').count() == 1:
		extends = 'base/admin_nav.html'
		
	return render(request, "reportes/eje.html", {"extends": extends,
													 "title": title, 
													 "politicas": politicas,
													 "ejes": ejes,
													 "headers": headers,
													 "respuestas": respuestas
													 })


@login_required()
def reporte_programa_view(request):
	title = "Reporte general"
	if request.user.groups.filter(name='Administrador').count() == 1:
		politicas = PoliticaPublica.objects.all()
		programas = Programa.objects.all().order_by('id')
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
				relacion = IndicadorEntidad.objects.filter(indicador__id=item.indicador.id).select_related('subprograma').first() 
				if relacion.subprograma is not None:
					programa = Programa.objects.filter(id=relacion.subprograma.programa_id).first()
					if programa is not None:
						with connection.cursor() as cursor:
							cursor.execute("SELECT seguimiento_pregunta.id, SUM(seguimiento_respuesta.valor::INTEGER) AS sumatoria FROM seguimiento_formulariorespuesta INNER JOIN seguimiento_respuesta ON seguimiento_respuesta.formulario_respuesta_id = seguimiento_formulariorespuesta.id INNER JOIN seguimiento_pregunta ON seguimiento_respuesta.pregunta_id = seguimiento_pregunta.id INNER JOIN seguimiento_indicador ON seguimiento_respuesta.indicador_id = seguimiento_indicador.id INNER JOIN seguimiento_indicadorentidad ON seguimiento_indicadorentidad.indicador_id = seguimiento_indicador.id INNER JOIN seguimiento_subprograma ON seguimiento_indicadorentidad.subprograma_id = seguimiento_subprograma.id INNER JOIN seguimiento_programa ON seguimiento_subprograma.programa_id = seguimiento_programa.id WHERE seguimiento_formulariorespuesta.id = %s AND seguimiento_programa.id = %s AND seguimiento_pregunta.id IN (9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,26, 27, 28, 29, 30, 31, 32, 33, 34, 35,36, 37, 38, 39) GROUP BY seguimiento_programa.id, seguimiento_pregunta.id order by seguimiento_pregunta.id", [formulario.id, programa.id])
							rows = cursor.fetchall()
							rows = dict(rows)
							if rows is not None:
								if formulario.politica_publica.id not in respuestas:
									respuestas[formulario.politica_publica.id] = {}
								respuestas[formulario.politica_publica.id][programa.id] = rows

	if request.user.groups.filter(name='Administrador').count() == 1:
		extends = 'base/admin_nav.html'
		
	return render(request, "reportes/programa.html", {"extends": extends,
													 "title": title, 
													 "politicas": politicas,
													 "programas": programas,
													 "headers": headers,
													 "respuestas": respuestas
													 })


@login_required()
def reporte_subprograma_view(request):
	title = "Reporte general"
	if request.user.groups.filter(name='Administrador').count() == 1:
		politicas = PoliticaPublica.objects.all()
		subprogramas = Subprograma.objects.all().order_by('id')
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
				relacion = IndicadorEntidad.objects.filter(indicador__id=item.indicador.id).first() 
				if relacion.subprograma is not None:
					with connection.cursor() as cursor:
						cursor.execute("SELECT seguimiento_pregunta.id, SUM(seguimiento_respuesta.valor::INTEGER) AS sumatoria FROM seguimiento_formulariorespuesta INNER JOIN seguimiento_respuesta ON seguimiento_respuesta.formulario_respuesta_id = seguimiento_formulariorespuesta.id INNER JOIN seguimiento_pregunta ON seguimiento_respuesta.pregunta_id = seguimiento_pregunta.id INNER JOIN seguimiento_indicador ON seguimiento_respuesta.indicador_id = seguimiento_indicador.id INNER JOIN seguimiento_indicadorentidad ON seguimiento_indicadorentidad.indicador_id = seguimiento_indicador.id INNER JOIN seguimiento_subprograma ON seguimiento_indicadorentidad.subprograma_id = seguimiento_subprograma.id WHERE seguimiento_formulariorespuesta.id = %s AND seguimiento_subprograma.id = %s AND seguimiento_pregunta.id IN (9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,26, 27, 28, 29, 30, 31, 32, 33, 34, 35,36, 37, 38, 39) GROUP BY seguimiento_subprograma.id, seguimiento_pregunta.id order by seguimiento_pregunta.id", [formulario.id, relacion.subprograma.id])
						rows = cursor.fetchall()
						rows = dict(rows)
						if rows is not None:
							if formulario.politica_publica.id not in respuestas:
								respuestas[formulario.politica_publica.id] = {}
							respuestas[formulario.politica_publica.id][relacion.subprograma.id] = rows

	if request.user.groups.filter(name='Administrador').count() == 1:
		extends = 'base/admin_nav.html'
		
	return render(request, "reportes/subprograma.html", {"extends": extends,
													 "title": title, 
													 "politicas": politicas,
													 "subprogramas": subprogramas,
													 "headers": headers,
													 "respuestas": respuestas
													 })


@login_required()
def reporte_avance_view(request):
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
	headers = []
	avance = Pregunta.objects.filter(id=7).first()
	headers.append(avance.enunciado)
	headers.append("Meta de la política")
	headers.append("Porcentaje de avance")

	formularios = FormularioRespuesta.objects.filter(vigencia=vigencia).filter(estado='aprobado').prefetch_related('respuesta_set')
	respuestas = {}

	for i in formularios:
		for j in politicas:
			if i.politica_publica == j:
				respuestas[j.id] = {}
				for k in indicadores:
					respuestas[j.id][k.id] = {}
					respuestas[j.id][k.id]['avance'] = i.respuesta_set.filter(indicador=k).filter(indicador__politica_publica=j).filter(pregunta=avance).order_by('pregunta')
					respuestas[j.id][k.id]['meta'] = k.meta
					if respuestas[j.id][k.id]['avance'] is not None and respuestas[j.id][k.id]['meta'] is not None:
						respuestas[j.id][k.id]['porcentaje'] = (float(respuestas[j.id][k.id]['avance'][0].valor) / float(respuestas[j.id][k.id]['meta'])) * 100

	if request.user.groups.filter(name='Administrador').count() == 1:
		extends = 'base/admin_nav.html'
	elif request.user.groups.filter(name='Operador').count() == 1:
		extends = 'base/user_nav.html'
		
	return render(request, "reportes/avance.html", {"extends": extends,
													 "title": title, 
													 "politicas": politicas,
													 "indicadores": indicadores,
													 "headers": headers,
													 "respuestas": respuestas
													 })