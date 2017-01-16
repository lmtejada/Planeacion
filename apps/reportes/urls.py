from django.conf.urls import url
from apps.reportes.views import (
	reporte_general_view,
	reporte_politicas_view,
	reporte_nivel1_view,
	reporte_nivel2_view,
	reporte_nivel3_view,
	reporte_eje_view,
	reporte_programa_view,
	reporte_subprograma_view,
	reporte_avance_view
)

urlpatterns = [
	url(r'^general/', reporte_general_view, name='general'),
	url(r'^avance/', reporte_avance_view, name='avance'),
	url(r'^politicas/', reporte_politicas_view, name='politicas'),
	url(r'^nivel1/', reporte_nivel1_view, name='nivel1'),
	url(r'^nivel2/', reporte_nivel2_view, name='nivel2'),
	url(r'^nivel3/', reporte_nivel3_view, name='nivel3'),
	url(r'^eje/', reporte_eje_view, name='eje'),
	url(r'^programa/', reporte_programa_view, name='programa'),
	url(r'^subprograma/', reporte_subprograma_view, name='subprograma'),
]