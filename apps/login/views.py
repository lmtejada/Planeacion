from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
		authenticate,
		get_user_model,
		login,
		logout,
	)
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from apps.login.forms import LoginForm

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

def register_view(request):
	return render(request, "login.html", {})

@login_required()
def home_view(request):
	return render(request, "login/home.html")