from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout

def index(request):
    #checking anonymous user
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request,'index.html')

def login_user(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return render(request,'login.html')
    
    return render(request,'login.html')

def logout_user(request):
    logout(request)
    return redirect("/login")
