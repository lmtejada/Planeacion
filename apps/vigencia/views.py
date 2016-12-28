from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from apps.seguimiento.models import Formulario, Vigencia
from apps.vigencia.forms import VigenciaForm
from django.contrib import messages
from datetime import datetime

# Create your views here.
@user_passes_test(lambda u: u.groups.filter(name='Administrador').count() == 1)
def asignar_view(request):
	title = "Asignar vigencia"
	formularios = Formulario.objects.all()

	vigenciaform = VigenciaForm(request.POST or None)

	if vigenciaform.is_valid():
		anio = request.POST['anio']
		semestre = request.POST['semestre']
		inicio = request.POST['fecha_inicio']
		fin = request.POST['fecha_fin']
		fecha_actual = datetime.now()
		fecha_inicio = datetime.strptime(inicio, '%Y-%m-%d')
		fecha_fin = datetime.strptime(fin, '%Y-%m-%d')

		if fecha_inicio.date() == fecha_fin.date():
			messages.add_message(request, messages.ERROR, 'Las fechas de inicio y de fin no deben ser iguales')
			return render(request, "vigencia/asignar.html", {"vigenciaform": vigenciaform, 
													"title": title,
													"formularios": formularios})

		if fecha_fin.date() < fecha_inicio.date():
			messages.add_message(request, messages.ERROR, 'La fecha de fin no debe ser anterior a la fecha de inicio')
			return render(request, "vigencia/asignar.html", {"vigenciaform": vigenciaform, 
													"title": title,
													"formularios": formularios})

		if fecha_inicio.date() < fecha_actual.date() or fecha_fin.date() < fecha_actual.date():
			messages.add_message(request, messages.ERROR, 'Las fechas no deben ser anteriores a la fecha actual')
			return render(request, "vigencia/asignar.html", {"vigenciaform": vigenciaform, 
													"title": title,
													"formularios": formularios})

		formActivo = Vigencia.objects.filter(formulario__id=request.POST['formulario']).filter(activo=True).first()
		if formActivo:
			formActivo.activo = False
			formActivo.save()

		vigencia = vigenciaform.save(commit=False)
		vigencia.periodo = anio + "-" + semestre
		vigencia.save()
		messages.add_message(request, messages.SUCCESS, 'Vigencia asignada exitosamente')
		return render(request, "vigencia/asignar.html", {"vigenciaform": vigenciaform, 
													"title": title,
													"formularios": formularios})

	return render(request, "vigencia/asignar.html", {"vigenciaform": vigenciaform, 
													"title": title,
													"formularios": formularios})

'''
	if form.is_valid() and personaForm.is_valid():
		usuario = form.save(commit=False)
		usuario.set_password(form.cleaned_data.get("password"))
		usuario.save()
		usuario.groups.add(Group.objects.get(name='Operador'))
		persona  = personaForm.save(commit=False)
		persona.user = usuario
		persona.save()
		return redirect('cuenta:home')

	return render(request, "login/registro.html", {"form": form, 
												   "personaForm": personaForm, 
												   "entidades": entidades, 
												   "title": title})
'''