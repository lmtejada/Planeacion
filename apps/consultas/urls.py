from django.conf.urls import url
from apps.consultas.views import (
	listado_view,
	detalle_view,
)

urlpatterns = [

    url(r'^formularios/', listado_view, name='formularios'),
    url(r'^detalle/(?P<pk>\d+)/$', detalle_view, name='detalle'),
]
