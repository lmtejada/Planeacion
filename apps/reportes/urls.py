from django.conf.urls import url
from apps.reportes.views import (
	reporte_general_view,
)

urlpatterns = [

    url(r'^general/', reporte_general_view, name='general'),
]
