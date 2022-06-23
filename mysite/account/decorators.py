from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Postion
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard', request.user.username)
        else:
            return view_func(request, *args, **kwargs)
        
    return wrapper_func


def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			group = None
			if request.user.profile.position:
				group = Postion.objects.get(id=request.user.profile.position.id)

			if group.position == allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('You do not have permissions!!!')
		return wrapper_func
	return decorator
