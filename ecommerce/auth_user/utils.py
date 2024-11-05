from django.shortcuts import redirect

def redirect_authenticated_user(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')  # Replace 'home' with the desired redirect URL name
        return view_func(request, *args, **kwargs)
    return wrapper
