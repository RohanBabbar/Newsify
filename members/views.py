from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

def login_user(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.success(request, ("Try again!!"))
            return redirect('/members/login_user')
    else:
        return render(request, 'authenticate/login.html', {})
    

def logout_user(request):
    logout(request)
    messages.success(request, ("Logged out successfully"))
    return redirect('/')
