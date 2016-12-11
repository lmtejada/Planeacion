from django.conf.urls import url
from apps.seguimiento.views import inicio, form_view, get_data_view

urlpatterns = [

    url(r'^$', inicio, name='index'),
    url(r'^formulario/', form_view, name='crear_formulario'),
    url(r'^get_data/', get_data_view, name='get_data'),
]
