from django.shortcuts import render,redirect,HttpResponse

# Create your views here.


# views.py
from .utils import redirect_authenticated_user
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from django.contrib.auth import authenticate, login,logout

# views.py
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'login.html', {
            'success_message': "Your account has been activated successfully! Please log in."
        })
    else:
        return render(request, 'login.html', {
            'error_message': "Activation link is invalid. Please try again."
        })

def signUp(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_repeat = request.POST.get('password_repeat')

        if password != password_repeat:
            return render(request, 'signUp.html', {
                'error_message': "Passwords do not match. Please try again."
            })

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return render(request, 'signUp.html', {
                'error_message': "Email already exists. Please try another email."
            })

        # Create the user with is_active=False
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False
        user.save()

        # Generate token and uid for email activation link
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Build activation link
        activation_link = request.build_absolute_uri(f'/auth/activate/{uid}/{token}/')

        # Send activation email
        send_mail(
            'Activate Your Account',
            f'Hello {username},\n\nPlease click the link below to activate your account:\n{activation_link}',
            'from@example.com',
            [email],
            fail_silently=False,
        )

        return render(request, 'login.html', {
            'success_message': "Signup successful! Please check your email to activate your account."
        })

    return render(request, "signUp.html")

   

@redirect_authenticated_user
def signIn(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Find user by email
        try:
            username = User.objects.get(email=email).username
        except User.DoesNotExist:
            return render(request, 'login.html', {
                'error_message': "User with this email does not exist."
            })


    
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'index.html', {
                    'success_message': "Login successful!"
                })
            else:
                return render(request, 'login.html', {
                    'error_message': "Your account is not activated. Please check your email."
                })
        else:
            return render(request, 'login.html', {
                'error_message': "Invalid email or password. Please try again."
            })

    return render(request, "login.html")

def signOut(request):
    logout(request)
    return redirect("/auth/signIn")