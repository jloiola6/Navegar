from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse

def user_type_required(user_type):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Verifique o tipo do usuário
            if request.user.type != user_type:
                return redirect(reverse('core:index'))
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def redirect_authenticated_user(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Se o usuário já estiver autenticado, redirecione para o index
        if request.user.is_authenticated:
            return redirect('core:index')  # Substitua 'core:index' pela sua URL desejada
        return view_func(request, *args, **kwargs)

    return _wrapped_view