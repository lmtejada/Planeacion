from django.db import models
from django.contrib.auth.models import User

TIPO_PREGUNTA = (
    ('0', 'text'),
    ('1', 'number'),
    ('2', 'select'),
)

class Entidad(models.Model):
	id = models.IntegerField(primary_key=True)
	nombre = models.CharField(max_length=200)

	def __str__(self):
		return '{}'.format(self.nombre)

class Persona(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=200)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)

	def __str__(self):
		return '{}'.format(self.nombre)

class PoliticaPublica(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=200)
	alias = models.CharField(max_length=30)
	objetivo = models.TextField()

	def __str__(self):
		return '{}'.format(self.nombre)

class EjeEstrategico(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=200)
	codigo = models.CharField(max_length=5)

	def __str__(self):
		return '{}'.format(self.nombre)

class Programa(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=200)
	codigo = models.CharField(max_length=5)
	eje_estrategico = models.ForeignKey(EjeEstrategico, on_delete=models.CASCADE)

	def __str__(self):
		return '{}'.format(self.nombre)

class Subprograma(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=200)
	codigo = models.CharField(max_length=5)
	programa = models.ForeignKey(Programa, on_delete=models.CASCADE)

	def __str__(self):
		return '{}'.format(self.nombre)

class Proyecto(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=200)
	codigo = models.CharField(max_length=10)
	subprograma = models.ForeignKey(Subprograma, on_delete=models.CASCADE)

	def __str__(self):
		return '{}'.format(self.nombre)

class Indicador(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=200)
	politica_publica = models.ForeignKey(PoliticaPublica, on_delete=models.CASCADE) 
	entidad = models.ManyToManyField(Entidad)
	proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)

	def __str__(self):
		return '{}'.format(self.nombre)

class Formulario(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=200)
	politica = models.OneToOneField(PoliticaPublica, null=True, on_delete=models.SET_NULL)

	def __str__(self):
		return '{}'.format(self.nombre)

class FormularioRespuesta(models.Model):
	id = models.AutoField(primary_key=True)
	fecha = models.DateTimeField(auto_now_add=True)
	entidad = models.OneToOneField(Entidad, on_delete=models.PROTECT)
	indicador = models.OneToOneField(Indicador, on_delete=models.PROTECT)

	def __str__(self):
		return '{} - {} - {}'.format(self.entidad, self.indicador, self.fecha)

class Pregunta(models.Model):
	id = models.AutoField(primary_key=True)
	enunciado = models.TextField()
	tipo_pregunta = models.CharField(max_length=1, choices=TIPO_PREGUNTA)
	formulario = models.ForeignKey(Formulario, on_delete=models.PROTECT)

	def __str__(self):
		return '{}'.format(self.enunciado)

class Respuesta(models.Model):
	id = models.AutoField(primary_key=True)
	valor = models.TextField()
	pregunta = models.OneToOneField(Pregunta, on_delete=models.PROTECT)
	formulario_respuesta = models.ForeignKey(FormularioRespuesta, on_delete=models.PROTECT)

	def __str__(self):
		return '{}'.format(self.valor)