from django.conf.urls import url
from apps.seguimiento.views import inicio, CrearFormulario

urlpatterns = [

    url(r'^$', inicio, name='index'),
    url(r'^formulario/', CrearFormulario.as_view(), name='crear_formulario'),
]
