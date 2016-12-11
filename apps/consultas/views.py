from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from apps.seguimiento.models import FormularioRespuesta

# Create your views here.

@login_required()
def listado_view(request):
	if request.user.groups.filter(name='Administrador').count() == 1:
		extends = 'base/admin_nav.html'
	else:
		extends = 'base/user_nav.html'

	formulariorespuestas = FormularioRespuesta.objects.all()

	return render(request, "consultas/listado_formularios.html", {"extends": extends,
																"formulariorespuestas": formulariorespuestas})
