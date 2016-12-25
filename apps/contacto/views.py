from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

# Create your views here.
@login_required()
def contacto_view(request):
	if request.user.groups.filter(name='Administrador').count() == 1:
		extends = 'base/admin_nav.html'
	else:
		extends = 'base/user_nav.html'

	return render(request, "contacto/contacto.html", {"extends": extends})
