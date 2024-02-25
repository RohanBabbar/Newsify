from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import get_object_or_404, render, redirect
# from django.views.generic import ListView, DetailView
#ListView allows a query set into a database and brings back the details of all the records while DetailView brings back the details of one record
import requests
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from bs4 import BeautifulSoup
from .models import Contact, Article
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import Http404


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

# def blog(request):
#     return render(request, 'myapp/blog.html')
class blog(ListView):
    model = Post
    template_name = 'myapp/blog.html'
    queryset = Post.objects.filter(approved=True)

class BlogDetail(DetailView):
    model = Post
    template_name = 'myapp/blog_detail.html'

class AddPostView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'myapp/add_post.html'
    fields = '__all__'
    login_url = 'members:login'

    def handle_no_permission(self):
        messages.warning(self.request, 'Login is required to add a post.')
        return super().handle_no_permission()
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.approved = False  # Set the default approval status
        messages.success(self.request, 'Your post has been submitted for review.')
        return super().form_valid(form)
    

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
# views.py


def category_list(request, category):
    news_api_key = '81ee455129704276a4b2e5baed4a07c1'

    country_code = 'in'
    news_url = f'https://newsapi.org/v2/top-headlines?country={country_code}&category={category}&apiKey={news_api_key}'

    try:
        response = requests.get(news_url)
        response.raise_for_status()  

        articles = response.json().get('articles', [])
        article_urls = [article.get('url') for article in articles]

        like_counts = request.session.get('like_counts', {})
        dislike_counts = request.session.get('dislike_counts', {})

        for article in articles:
        # Retrieve like and dislike counts for each article
            article_identifier = article.get('url', '')
            article['likes'] = like_counts.get(article_identifier, 0)
            article['dislikes'] = dislike_counts.get(article_identifier, 0)

        return render(request, 'myapp/category_list.html', {'article_urls': article_urls, 'articles': articles})

    except requests.RequestException as e:
        error_message = f"Failed to fetch news data: {str(e)}"
        return render(request, 'myapp/error_page.html', {'error_message': error_message})

def like_dislike_article(request, article_identifier):
    
    if request.method == 'POST':
        action = request.POST.get('action')
        user_id = request.user.id
        print("iddddddd" + str(user_id))
        article_identifier = str(article_identifier)


        if request.user.is_authenticated:
        # Retrieve like and dislike counts from the session
            like_counts = request.session.get('like_counts', {})
            dislike_counts = request.session.get('dislike_counts', {})
            #NEW
            user_likes = like_counts.get(article_identifier, [])
            user_dislikes = dislike_counts.get(article_identifier, [])
            
            if action == 'like' and user_id not in user_likes and user_id not in user_dislikes:
                user_likes.append(user_id)
            elif action == 'dislike' and user_id not in user_likes and user_id not in user_dislikes:
                user_dislikes.append(user_id)
            like_counts[article_identifier] = user_likes
            dislike_counts[article_identifier] = user_dislikes
            request.session['like_counts'] = like_counts
            request.session['dislike_counts'] = dislike_counts



            # if user_id not in [user_likes] and user_id not in [user_dislikes]:
            #     # if action == 'like':
            #     #     like_counts[article_identifier] = like_counts.get(article_identifier, 0) + 1
            #     # elif action == 'dislike' :
            #     #     dislike_counts[article_identifier] = dislike_counts.get(article_identifier, 0) + 1
            #     if action == 'like':
            #         like_counts[article_identifier] = user_likes + [user_id]
            #     elif action == 'dislike':
            #         dislike_counts[article_identifier] = user_dislikes + [user_id]

        # Save the updated like and dislike counts in the session
                # request.session['like_counts'] = like_counts 
                # request.session['dislike_counts'] = dislike_counts
        

    # Redirect back to the original page
    # return render(request, 'myapp/category_list.html', {'article_urls': article_identifier, 'articles': articles})
            return redirect('myapp:category_list', category='general')
        else:
            return redirect('/members/login_user')
    

def article_list(request):
    # Fetch a list of articles from the database
    articles = Article.objects.all()
    for article in articles:
        print(article.id)  # Check if this prints the IDs in the console
    return render(request, 'myapp/article_list.html', {'articles': articles})

# def article_detail(request, article_id):
#     news_api_key = '81ee455129704276a4b2e5baed4a07c1'
#     news_url = f'https://newsapi.org/v2/everything?q={article_id}&apiKey={news_api_key}'
#     response = requests.get(news_url)
#     article_data = response.json().get('articles', [])
#     if article_data:
#         article_info = article_data[0]

#         # Extract relevant information from the API response
#         title = article_info.get('title', 'N/A')
#         content = article_info.get('content', 'N/A')

#         # Render the 'myapp/article_detail.html' template with the retrieved article details
#         return render(request, 'myapp/article_list.html', {'title': title, 'content': content})
#     else:
#         return render(request, 'myapp/article_not_found.html')
def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    country_code = 'in'

    # Construct the URL for fetching top headlines from the News API based on the category
    news_url = f'https://newsapi.org/v2/top-headlines?country={country_code}&category={category}&apiKey={news_api_key}'

    # Make a GET request to the News API
    response = requests.get(news_url)
    news = response.json().get('url', [])


    # Make a request to the article's URL to get its HTML content
    response = requests.get(article.url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the article content (adjust based on the HTML structure of the page)
        content = soup.find('div', class_='article-content')  # Replace 'article-content' with the actual class or tag

        # Render the 'myapp/article_detail.html' template with the retrieved article details
        return render(request, 'myapp/article_detail.html', {'article': article, 'content': content})
    else:
        # If the request was not successful, render an error template
        raise Http404("Article not found.")