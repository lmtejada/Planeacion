from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from apps.seguimiento.models import FormularioRespuesta
from apps.login.models import Persona

# Create your views here.

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
	
	idformulariorespuesta = FormularioRespuesta.objects.get(pk=int(pk))

	if request.user.groups.filter(name='Administrador').count() == 1:
		extends = 'base/admin_nav.html'
	elif request.user.groups.filter(name='Operador').count() == 1:
		extends = 'base/user_nav.html'

	return render(request, "consultas/detalle.html", {"extends": extends,
													"idformulariorespuesta": idformulariorespuesta})
