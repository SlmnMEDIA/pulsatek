from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model

def user_is_staff_only(function):
    def wrap(request, *args, **kwargs):
        userman = request.user
        if userman.is_superuser or userman.is_staff:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_agen_or_staff(function):
    def wrap(request, *args, **kwargs):
        userman = request.user
        if userman.is_superuser or userman.is_staff or userman.is_agen:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def user_is_referal_agen(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff :
            return function(request, *args, **kwargs)

        user_class = get_user_model()
        user_obj = user_class.objects.get(pk=kwargs['id'])
        if user_obj.leader == request.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

