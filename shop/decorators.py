from django.http import HttpResponse
from django.shortcuts import redirect

def just_owner(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.owner:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('add_shop')
        else:
            return redirect('register')
    return wrapper_func

def not_owner(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.owner:
                return redirect('shop', request.user.shop.slug)
            else:
                return view_func(request, *args, **kwargs)
        else:
            return redirect('register')
    return wrapper_func
