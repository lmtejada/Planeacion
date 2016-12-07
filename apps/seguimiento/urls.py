from django.conf.urls import url
from apps.seguimiento.views import inicio, form_view

urlpatterns = [

    url(r'^$', inicio, name='index'),
    url(r'^formulario/', form_view, name='crear_formulario'),
]
