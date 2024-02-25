from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login



def login_user(request):
    if request.method=="POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user=authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful")
                return redirect('/')
            else:
                messages.success(request, ("Try again!!"))
                return redirect('/members/login_user')
    else:
        form = AuthenticationForm()
    return render(request, 'authenticate/login.html', {})
    

def logout_user(request):
    logout(request)
    messages.success(request, ("Logged out successfully"))
    return redirect('/')

def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, "Registration completed")
                return redirect('/')
            else:
                messages.error(request, "Unable to log in after registration")
        else:
            messages.error(request, "Invalid registration form")
    else:
        form = UserCreationForm()

    return render(request, 'authenticate/register_user.html', {'form': form})