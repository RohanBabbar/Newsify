from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
#ListView allows a query set into a database and brings back the details of all the records while DetailView brings back the details of one record
import requests
from .models import Contact, Article
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")  
    else:
        form = UserCreationForm()

    return render(request, "myapp/register.html", {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage')  # Redirect to the home page after login
    else:
        form = AuthenticationForm()

    return render(request, 'myapp/login.html', {'form': form})

def home(request):
    return render(request, 'myapp/homepage.html')

def contact_form(request):
    if request.method=="POST":
        contact=Contact()
        name=request.POST.get('name')
        email=request.POST.get('email')
        subject=request.POST.get('comments')
        contact.name=name
        contact.email=email
        contact.subject=subject
        contact.save()
        return HttpResponse("Your message has been delivered")
    return render(request, 'myapp/contact_form.html')

def category_list(request, category):
    # Set the News API key
    news_api_key = '81ee455129704276a4b2e5baed4a07c1'

    # Construct the URL for fetching top headlines from the News API
    country_code = 'in'

    # Construct the URL for fetching top headlines from the News API based on the category
    news_url = f'https://newsapi.org/v2/top-headlines?country={country_code}&category={category}&apiKey={news_api_key}'

    # Make a GET request to the News API
    response = requests.get(news_url)

    # Extract the 'articles' field from the JSON response; default to an empty list if not present
    articles = response.json().get('articles', [])

    # Render the 'myapp/category_list.html' template with the retrieved articles
    return render(request, 'myapp/category_list.html', {'articles': articles, 'category': category})


