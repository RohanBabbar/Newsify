from django.urls import path
from .views import home, category_list, contact_form, article_detail
from .views import like_dislike_article, blog, BlogDetail, AddPostView


app_name = 'myapp'

urlpatterns = [
    path('', home, name='homepage'),
    path('blog/', blog.as_view(), name='blog'),
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('article/<int:pk>', BlogDetail.as_view(), name='blog-detail'),
    path('categories/<str:category>/', category_list, name='category_list'),
    path('article/<int:article_id>/', article_detail, name='article_detail'),
    path('like_dislike_article/<path:article_identifier>/', like_dislike_article, name='like_dislike_article'),
    path('contact/', contact_form, name='contact_form'),
    # path('articles/', article_list, name='article_list'),
    # path('register/', register, name='register'),
    # path('login/', user_login, name='login'),
]
