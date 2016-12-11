from django.conf.urls import url
from apps.seguimiento.views import form_view

urlpatterns = [

    url(r'^formulario/', form_view, name='formulario'),
]
