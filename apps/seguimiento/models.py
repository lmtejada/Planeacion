from django.db import models

GRUPOS = (
	('1', 'Plan de desarrollo'),
    ('2', 'Información general'),
    ('3', 'Recursos'),
    ('4', 'Población atendida'),
)

SUBGRUPOS = (
	('1', 'Género'),
    ('2', 'Zona'),
    ('3', 'Ciclos de edad'),
    ('4', 'Condición'),
    ('5', 'Etnia'),
)

TIPO_PREGUNTA = (
    ('text', 'Texto'),
    ('number', 'Numérico'),
    ('textarea', 'Cuadro de texto'),
)

ESTADO = (
    ('pendiente', 'Pendiente'),
    ('aprobado', 'Aprobado'),
    ('no_aprobado', 'No aprobado'),
)

NIVELES1 = (
    ('1', 'Línea orientadora'),
    ('2', 'Línea estratégica'),
    ('3', 'Categoría'),
    ('4', 'Objetivo estratégico'),
    ('5', 'Estrategia'),
    ('6', 'Objetivo de la política'),
)

NIVELES2 = (
    ('1', 'Categoría de la política'),
    ('2', 'Estrategia'),
    ('3', 'Objetivo de la política'),
    ('4', 'Acciones recomendadas'),
)

NIVELES3 = (
    ('1', 'Objetivo de la política'),
    ('2', 'Acciones recomendadas'),
    ('3', 'Estrategia'),
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
	objetivo = models.TextField(null=True)

	def __str__(self):
		return '{}'.format(self.nombre)

class EjeEstrategico(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=200)
	codigo = models.CharField(max_length=10)

	def __str__(self):
		return '{}'.format(self.nombre)

class Programa(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=200)
	codigo = models.CharField(max_length=10)
	eje_estrategico = models.ForeignKey(EjeEstrategico, on_delete=models.CASCADE)

	def __str__(self):
		return '{}'.format(self.nombre)

class Subprograma(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=200)
	codigo = models.CharField(max_length=10)
	programa = models.ForeignKey(Programa, on_delete=models.CASCADE)

	def __str__(self):
		return '{}'.format(self.nombre)

class Formulario(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=200)

	def __str__(self):
		return '{}'.format(self.nombre)

class Vigencia(models.Model):
	id = models.AutoField(primary_key=True)
	periodo = models.CharField(max_length=10)
	fecha_inicio = models.DateTimeField()
	fecha_fin = models.DateTimeField()
	activo = models.BooleanField(default=True)
	formulario = models.ForeignKey(Formulario, on_delete=models.PROTECT)

	def __str__(self):
		return '{}'.format(self.periodo)

class FormularioRespuesta(models.Model):
	id = models.AutoField(primary_key=True)
	fecha_envio = models.DateTimeField(null=True)
	estado = models.CharField(max_length=15, choices=ESTADO, null=True)
	enviado = models.BooleanField(default=False)
	activo = models.BooleanField(default=True)
	entidad = models.ForeignKey(Entidad, on_delete=models.PROTECT)
	vigencia = models.ForeignKey(Vigencia, on_delete=models.PROTECT)
	politica_publica = models.ForeignKey(PoliticaPublica, on_delete=models.PROTECT, null=True)

	def __str__(self):
		return '{} - {} - {}'.format(self.entidad, self.politica_publica, self.vigencia)

class Pregunta(models.Model):
	id = models.AutoField(primary_key=True)
	enunciado = models.TextField()
	grupo = models.CharField(max_length=2, choices=GRUPOS)
	subgrupo = models.CharField(max_length=2, choices=SUBGRUPOS, null=True)
	tipo_pregunta = models.CharField(max_length=10, choices=TIPO_PREGUNTA)
	formulario = models.ForeignKey(Formulario, on_delete=models.PROTECT)

	def __str__(self):
		return '{}'.format(self.enunciado)

class Nivel1(models.Model):
	id = models.AutoField(primary_key=True)
	texto = models.TextField()
	nivel = models.CharField(max_length=2, choices=NIVELES1)

	def __str__(self):
		return '{}'.format(self.texto)

class Nivel2(models.Model):
	id = models.AutoField(primary_key=True)
	texto = models.TextField()
	nivel = models.CharField(max_length=2, choices=NIVELES2)

	def __str__(self):
		return '{}'.format(self.texto)

class Nivel3(models.Model):
	id = models.AutoField(primary_key=True)
	texto = models.TextField()
	nivel = models.CharField(max_length=2, choices=NIVELES3)

	def __str__(self):
		return '{}'.format(self.texto)

class Indicador(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=200)
	politica_publica = models.ForeignKey(PoliticaPublica, on_delete=models.CASCADE) 
	entidad = models.ManyToManyField(Entidad, through='IndicadorEntidad')
	accion = models.TextField(null=True)
	meta = models.CharField(max_length=20, null=True)
	nivel1 = models.ForeignKey(Nivel1, on_delete=models.PROTECT, null=True)
	nivel2 = models.ForeignKey(Nivel2, on_delete=models.PROTECT, null=True)
	nivel3 = models.ForeignKey(Nivel3, on_delete=models.PROTECT, null=True)

	def __str__(self):
		return '{}'.format(self.nombre)

class Respuesta(models.Model):
	id = models.AutoField(primary_key=True)
	valor = models.TextField()
	pregunta = models.ForeignKey(Pregunta, on_delete=models.PROTECT)
	formulario_respuesta = models.ForeignKey(FormularioRespuesta, on_delete=models.PROTECT)
	indicador = models.ForeignKey(Indicador, on_delete=models.PROTECT)

	def __str__(self):
		return '{}'.format(self.valor)

class Observacion(models.Model):
	id = models.AutoField(primary_key=True)
	observacion = models.TextField()
	formulario_respuesta = models.ForeignKey(FormularioRespuesta, on_delete=models.PROTECT)
	indicador = models.ForeignKey(Indicador, on_delete=models.PROTECT)

	def __str__(self):
		return '{}'.format(self.observacion)	


class IndicadorEntidad(models.Model):
	id = models.AutoField(primary_key=True)
	indicador = models.ForeignKey(Indicador, on_delete=models.PROTECT)
	entidad = models.ForeignKey(Entidad, on_delete=models.PROTECT)
	subprograma = models.ForeignKey(Subprograma, on_delete=models.PROTECT, null=True)

	def __str__(self):
		return '{} - {}'.format(self.entidad, self.indicador)