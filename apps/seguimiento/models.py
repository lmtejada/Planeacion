from django.db import models

TIPO_PREGUNTA = (
    ('text', 'Texto'),
    ('number', 'Numérico'),
    ('select', 'Selector'),
    #('textarea', 'Cuadro de texto'),
)

ESTADO = (
    ('pendiente', 'Pendiente'),
    ('aprobado', 'Aprobado'),
    ('no_aprobado', 'No aprobado'),
)

class Entidad(models.Model):
	id = models.IntegerField(primary_key=True)
	nombre = models.CharField(max_length=200)

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
	#accion = models.TextField()
	politica_publica = models.ForeignKey(PoliticaPublica, on_delete=models.CASCADE) 
	entidad = models.ManyToManyField(Entidad)
	proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)

	def __str__(self):
		return '{}'.format(self.nombre)

class Formulario(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=200)

	def __str__(self):
		return '{}'.format(self.nombre)

class Vigencia(models.Model):
	id = models.AutoField(primary_key=True)
	periodo = models.CharField(max_length=10, unique=True)
	fecha_inicio = models.DateTimeField()
	fecha_fin = models.DateTimeField()
	activo = models.BooleanField(default=True)
	formulario = models.ForeignKey(Formulario, on_delete=models.PROTECT)

	def __str__(self):
		return '{}'.format(self.periodo)

class FormularioRespuesta(models.Model):
	id = models.AutoField(primary_key=True)
	fecha_envio = models.DateTimeField(null=True)
	estado = models.CharField(max_length=15, choices=ESTADO)
	enviado = models.BooleanField(default=False)
	activo = models.BooleanField(default=True)
	observaciones = models.TextField(null=True)
	entidad = models.ForeignKey(Entidad, on_delete=models.PROTECT)
	vigencia = models.ForeignKey(Vigencia, on_delete=models.PROTECT)

	def __str__(self):
		return '{} - {} - {}'.format(self.entidad, self.vigencia, self.fecha_envio)

class Pregunta(models.Model):
	id = models.AutoField(primary_key=True)
	enunciado = models.TextField()
	tipo_pregunta = models.CharField(max_length=10, choices=TIPO_PREGUNTA)
	formulario = models.ForeignKey(Formulario, on_delete=models.PROTECT)

	def __str__(self):
		return '{}'.format(self.enunciado)

class Respuesta(models.Model):
	id = models.AutoField(primary_key=True)
	valor = models.TextField()
	pregunta = models.ForeignKey(Pregunta, on_delete=models.PROTECT)
	formulario_respuesta = models.ForeignKey(FormularioRespuesta, on_delete=models.PROTECT)
	indicador = models.ForeignKey(Indicador, on_delete=models.PROTECT)

	def __str__(self):
		return '{}'.format(self.valor)