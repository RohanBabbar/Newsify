from django.urls import path
from .views import home, category_list, contact_form

app_name = 'myapp'

urlpatterns = [
    path('', home, name='homepage'),
    path('categories/<str:category>/', category_list, name='category_list'),
    path('contact/', contact_form, name='contact_form'),
]
