from django.conf.urls import url
from apps.reportes.views import (
	reporte_general_view,
	reporte_politicas_view,
	reporte_nivel1_view
)

urlpatterns = [
	url(r'^general/', reporte_general_view, name='general'),
	url(r'^politicas/', reporte_politicas_view, name='politicas'),
	url(r'^nivel1/', reporte_nivel1_view, name='nivel1'),
]