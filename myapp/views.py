from django.shortcuts import render
from django.views.generic import ListView, DetailView
#ListView allows a query set into a database and brings back the details of all the records while DetailView brings back the details of one record
import requests
from .models import Contact, Article
from django.http import HttpResponse

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


