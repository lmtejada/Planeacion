from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import prefetch_related_objects
from apps.seguimiento.models import FormularioRespuesta, Indicador, Respuesta, Pregunta, PoliticaPublica, Vigencia
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
	formularios = FormularioRespuesta.objects.filter(vigencia=vigencia).prefetch_related('respuesta_set')
	respuestas = {}
	niveles = {}

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

	for i in formularios:
		politica = PoliticaPublica.objects.filter(formulariorespuesta__id=i.id).first()
		respuestas[politica.id] = {}
		for j in indicadores:
			respuestas[politica.id][j.id] = i.respuesta_set.filter(indicador=j).filter(indicador__politica_publica=politica.id).order_by('pregunta')
			niveles[j.politica_publica.id] = {}

			print (respuestas[politica.id][j.id])
			
			nivel1 = Indicador.objects.filter(id=j.id).select_related('nivel1').first()
			if nivel1.nivel1 is not None:
				niveles[j.politica_publica.id]['nivel1'] = niveles1[nivel1.nivel1.nivel]
			else: 
				niveles[j.politica_publica.id]['nivel1'] = "Nivel 1"
			
			nivel2 = Indicador.objects.filter(id=j.id).select_related('nivel2').first()
			if nivel2.nivel2 is not None:
				niveles[j.politica_publica.id]['nivel2'] = niveles2[nivel2.nivel2.nivel]
			else: 
				niveles[j.politica_publica.id]['nivel2'] = "Nivel 2"

			nivel3 = Indicador.objects.filter(id=j.id).select_related('nivel3').first()
			if nivel3.nivel3 is not None:
				niveles[j.politica_publica.id]['nivel3'] = niveles3[nivel3.nivel3.nivel]
			else:
				niveles[j.politica_publica.id]['nivel3'] = "Nivel 3"

	#print (respuestas)
	
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
													 "niveles": niveles
													 })