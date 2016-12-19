from django.conf.urls import url
from apps.reportes.views import (
	reporte_general_view,
	reporte_general2_view,
	reporte_general3_view,
)

urlpatterns = [

    url(r'^general/', reporte_general_view, name='general'),
    url(r'^general2/', reporte_general2_view, name='general2'),
    url(r'^general3/', reporte_general3_view, name='general3'),
]
