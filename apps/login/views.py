from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, User
from django.contrib.auth import (
		authenticate,
		get_user_model,
		login,
		logout,
	)
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from apps.login.forms import LoginForm, UserRegisterForm, PersonaForm
from apps.seguimiento.models import Entidad

# Agregar la parte del next
def login_view(request):
	title = "Iniciar sesión"
	form = LoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username=username, password=password)
		login(request, user)
		return redirect('cuenta:home')
	return render(request, "login/login.html", {"form": form, "title": title})

def logout_view(request):
	logout(request)
	return redirect('cuenta:login')

# Validar que el correo no exista
@user_passes_test(lambda u: u.groups.filter(name='Administrador').count() == 1)
def register_view(request):
	title = "Registrar usuario"
	form = UserRegisterForm(request.POST or None)
	personaForm = PersonaForm(request.POST or None)
	entidades = Entidad.objects.all()

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

@login_required()
def home_view(request):
	if request.user.groups.filter(name='Administrador').count() == 1:
		extends = 'base/admin_nav.html'
	else:
		extends = 'base/user_nav.html'

	return render(request, "login/home.html", {"extends": extends})