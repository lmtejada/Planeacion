from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import prefetch_related_objects
from apps.seguimiento.models import FormularioRespuesta, Indicador
from apps.login.models import Persona

# Create your views here.

@login_required()
def reporte_general_view(request):

	if request.user.groups.filter(name='Administrador').count() == 1:
		extends = 'base/admin_nav.html'
		return render(request, "reportes/general.html", {"extends": extends})
	elif request.user.groups.filter(name='Operador').count() == 1:
		extends = 'base/user_nav.html'
		return render(request, "reportes/general.html", {"extends": extends})

	return redirect('cuenta:home')
