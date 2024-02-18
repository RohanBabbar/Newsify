from django.urls import path
from .views import home, category_list, contact_form
from .views import register, user_login


app_name = 'myapp'

urlpatterns = [
    path('', home, name='homepage'),
    path('categories/<str:category>/', category_list, name='category_list'),
    path('contact/', contact_form, name='contact_form'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
]
