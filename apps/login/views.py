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
from django.http import HttpResponse, JsonResponse
from django.core.urlresolvers import reverse_lazy
from apps.login.forms import LoginForm, UserRegisterForm, PersonaForm, EditUserForm, EditPersonaForm
from apps.seguimiento.models import Entidad
from apps.login.models import Persona
from django.db.models import prefetch_related_objects
from django.views.decorators.csrf import csrf_exempt

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
		nombre = request.POST['nombre']
		email = request.POST['email']
		password = editUserForm.cleaned_data.get("password")
		newPassword = request.POST['new_password']
		againPassword = request.POST['again_password']

		if nombre and nombre != persona.nombre:
			persona.nombre = nombre
			persona.save()

		if email and email != usuario.email:
			usuario.email = email
			usuario.save()

		if password:
			if usuario.check_password(password):
				if newPassword:
					if newPassword == againPassword:
						if len(newPassword) >= 8:
							usuario.set_password(newPassword)
							usuario.save()
						else:
							messages.add_message(request, messages.ERROR, 'La nueva contraseña es demasiado corta.')
							return render(request, "login/gestionar.html", {"extends": extends,
															"title": title,
															"usuario": usuario,
															"persona": persona,
															"editUserForm": editUserForm,
															"editPersonaForm": editPersonaForm})

					else:
						messages.add_message(request, messages.ERROR, 'Las contraseñas no coinciden.')
						return render(request, "login/gestionar.html", {"extends": extends,
															"title": title,
															"usuario": usuario,
															"persona": persona,
															"editUserForm": editUserForm,
															"editPersonaForm": editPersonaForm})

				else:
					messages.add_message(request, messages.ERROR, 'Debe diligenciar la nueva contraseña.')
					return render(request, "login/gestionar.html", {"extends": extends,
															"title": title,
															"usuario": usuario,
															"persona": persona,
															"editUserForm": editUserForm,
															"editPersonaForm": editPersonaForm})

			else:
				messages.add_message(request, messages.ERROR, 'Contraseña incorrecta.')
				return render(request, "login/gestionar.html", {"extends": extends,
															"title": title,
															"usuario": usuario,
															"persona": persona,
															"editUserForm": editUserForm,
															"editPersonaForm": editPersonaForm})
		elif newPassword or againPassword:
			messages.add_message(request, messages.ERROR, 'Para cambiar su contraseña debe indicar su contraseña actual.')
			return render(request, "login/gestionar.html", {"extends": extends,
															"title": title,
															"usuario": usuario,
															"persona": persona,
															"editUserForm": editUserForm,
															"editPersonaForm": editPersonaForm})
		
		return redirect('cuenta:home')

	return render(request, "login/gestionar.html", {"extends": extends,
														"title": title,
														"usuario": usuario,
														"persona": persona,
														"editUserForm": editUserForm,
														"editPersonaForm": editPersonaForm})

@user_passes_test(lambda u: u.groups.filter(name='Administrador').count() == 1)
def listado_view(request):
	title = "Listado de usuarios"

	#group = Group.objects.filter(name="Op")
	usuarios = User.objects.filter(groups__name="Operador")
	prefetch_related_objects(usuarios, 'persona')
	#print (usuarios[1].persona.entidad)
	#persona = Persona.objects.filter(user=usuario).first()

	return render(request, "login/listado.html", {"title": title,
												"usuarios": usuarios,})

@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name='Administrador').count() == 1)
def eliminar_view(request):
	if request.method == 'POST':
		id = request.POST['idUsuario'] 
		usuario = User.objects.filter(id=id)
		persona = Persona.objects.filter(user=usuario)
		persona.delete()
		usuario.delete()

		response_data = {}
		response_data["result"] = {}
		response_data["result"] = "Correcto"
		return HttpResponse(
			JsonResponse(response_data)
		)
	else:
		return HttpResponse(
			JsonResponse({"error": "Solicitud no válida."})
		)
