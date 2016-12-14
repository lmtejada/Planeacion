from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, User
from django.contrib.auth import (
		authenticate,
		get_user_model,
		login,
		logout,
	)
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from apps.login.forms import LoginForm, UserRegisterForm, PersonaForm, EditUserForm, EditPersonaForm
from apps.seguimiento.models import Entidad
from apps.login.models import Persona

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

@login_required()
def gestionar_view(request):
	title = "Gestionar cuenta"
	editUserForm = EditUserForm(request.POST or None)
	editPersonaForm = EditPersonaForm(request.POST or None)
	usuario = request.user
	persona = Persona.objects.filter(user=usuario).first()

	if request.user.groups.filter(name='Administrador').count() == 1:
		extends = 'base/admin_nav.html'
	elif request.user.groups.filter(name='Operador').count() == 1:
		extends = 'base/user_nav.html'
	else:
		return redirect('cuenta:home')



	if editUserForm.is_valid() and editPersonaForm.is_valid():
		password = editUserForm.cleaned_data.get("password")

		if usuario.check_password(password):
			print("son iguales")
		else:
			messages.add_message(request, messages.ERROR, 'Contraseña incorrecta.')
			return render(request, "login/gestionar.html", {"extends": extends,
														"title": title,
														"usuario": usuario,
														"persona": persona,
														"editUserForm": editUserForm,
														"editPersonaForm": editPersonaForm})

		newPassword = request.POST['new_password']
		print(newPassword)
		againPassword = request.POST['again_password']
		print(againPassword)
		return redirect('cuenta:home')

	return render(request, "login/gestionar.html", {"extends": extends,
														"title": title,
														"usuario": usuario,
														"persona": persona,
														"editUserForm": editUserForm,
														"editPersonaForm": editPersonaForm})