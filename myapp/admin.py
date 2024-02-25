from django.contrib import admin
from .models import Category, Article, comment,Contact, Post

# Register your models here.

admin.site.register(Category)
admin.site.register(Post)

class AdminNews(admin.ModelAdmin):
    list_display=('title','category','pub_date')

admin.site.register(Article,AdminNews)

class AdminComment(admin.ModelAdmin):
    list_display=('news','email','comment','status')

# admin.site.register(comment,AdminComment)

admin.site.register(Contact)