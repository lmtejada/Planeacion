from django.db import models
from django.contrib.auth.models import User

# Create your models here.

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
'''
class Formulario(models.Model):
	id = models.AutoField(primary_key=True)
	idPolitica = models.ForeignKey(Politicapublica, on_delete=models.CASCADE)

class Pregunta(models.Model):
	id = models.AutoField(primary_key=True)
	idPolitica = models.ForeignKey(Politicapublica, on_delete=models.CASCADE)

class Respuesta(models.Model):
	id = models.AutoField(primary_key=True)
	idPolitica = models.ForeignKey(Politicapublica, on_delete=models.CASCADE)
'''
