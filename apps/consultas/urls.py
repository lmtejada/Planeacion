from django.conf.urls import url
from apps.consultas.views import (
	listado_view,
)

urlpatterns = [

    url(r'^formularios/', listado_view, name='formularios'),
]
