from django.shortcuts import render,redirect

# Create your views here.

def signIn(request):
    return render(request,"login.html")

def signUp(request):
    return render(request,"signUp.html")
def signOut(request):
    return redirect("/auth/signIn")