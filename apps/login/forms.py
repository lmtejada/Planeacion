from django import forms
from django.contrib.auth import (
		authenticate,
		get_user_model,
		login,
		logout,
	)
from apps.login.models import Persona

User = get_user_model()

class LoginForm(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(widget=forms.PasswordInput, required=True)

	def clean(self):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		
		user = authenticate(username=username, password=password)
		if username and password:
			if not user:
				raise forms.ValidationError("Usuario y contraseña no válidos")
		else:
			raise forms.ValidationError("Debe indicar un nombre de usuario y contraseña válidos")
		return self.cleaned_data

class UserRegisterForm(forms.ModelForm):
	email = forms.CharField(required=True)
	password = forms.CharField(widget=forms.PasswordInput, required=True)

	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'password'
		]

class PersonaForm(forms.ModelForm):
	class Meta:
		model = Persona
		fields = [
			'nombre',
			'entidad'
		]




