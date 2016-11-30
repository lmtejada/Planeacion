from django.db import models
from django.contrib.auth.models import User

class Entidad(models.Model):
	id = models.IntegerField(primary_key=True)
	nombre = models.CharField(max_length=200)

class Persona(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE, default=3)
	entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)

class PoliticaPublica(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=200)
	objetivo = models.TextField()

class Indicador(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=200)
	politica_publica = models.ManyToManyField(PoliticaPublica) 
	entidad = models.ManyToManyField(Entidad)

class Formulario(models.Model):
	id = models.AutoField(primary_key=True)
	politica = models.OneToOneField(PoliticaPublica, null=True, on_delete=models.SET_NULL)

class FormularioRespuesta(models.Model):
	id = models.AutoField(primary_key=True)
	fecha = models.DateTimeField(auto_now_add=True)
	entidad = models.OneToOneField(Entidad, on_delete=models.PROTECT)
	indicador = models.OneToOneField(Indicador, on_delete=models.PROTECT)

class Pregunta(models.Model):
	id = models.AutoField(primary_key=True)
	enunciado = models.TextField()
	formulario = models.ForeignKey(Formulario, on_delete=models.PROTECT)

class Respuesta(models.Model):
	id = models.AutoField(primary_key=True)
	valor = models.TextField()
	pregunta = models.OneToOneField(Pregunta, on_delete=models.PROTECT)
	formulario_respuesta = models.ForeignKey(FormularioRespuesta, null=True, on_delete=models.PROTECT)

