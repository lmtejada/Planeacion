from django.conf.urls import url
from apps.consultas.views import (
	listado_view,
	detalle_view,
	get_data_view,
)

urlpatterns = [

    url(r'^formularios/', listado_view, name='formularios'),
    url(r'^detalle/(?P<pk>\d+)/$', detalle_view, name='detalle'),
    url(r'^get_data/', get_data_view, name='get_data'),
]
