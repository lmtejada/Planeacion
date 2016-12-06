from django.db import models
from apps.seguimiento.models import Entidad
from django.contrib.auth.models import User

class Persona(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=200)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)

	def __str__(self):
		return '{}'.format(self.nombre)
