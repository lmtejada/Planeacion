from django.conf.urls import url
from apps.login.views import (
	login_view,
	logout_view,
	register_view,
	home_view,
)

urlpatterns = [

    url(r'^login/', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^registrar/', register_view, name='registrar'),
    url(r'^home/', home_view, name='home'),
]
