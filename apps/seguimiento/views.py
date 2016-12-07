from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView
#from apps.seguimiento.forms import RespuestaForm
from django.core.urlresolvers import reverse_lazy
from apps.seguimiento.models import Entidad, PoliticaPublica

# Create your views here.

def inicio(request):
	politicas = PoliticaPublica.objects.all()
	entidades = Entidad.objects.all()

	#return HttpResponse("Index")
	return render(request, "seguimiento/index.html", {"entidades": entidades,
													"politicas": politicas})

def formulario(request):
	if request.method == 'POST':
		form = RespuestaForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect('seguimiento:index')
	else:
		form = RespuestaForm()

	return render(request, 'seguimiento/formulario.html', {'form': form})

class CrearFormulario(CreateView):
	#model = Infancia
	#form_class = RespuestaForm
	template_name = 'seguimiento/formulario.html'
	success_url = reverse_lazy('seguimiento:index')