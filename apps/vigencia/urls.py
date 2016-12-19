from django.conf.urls import url
from apps.vigencia.views import (
	asignar_view,
)

urlpatterns = [

    url(r'^asignar/', asignar_view, name='asignar'),
]
