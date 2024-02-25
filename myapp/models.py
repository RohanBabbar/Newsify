from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title + '|' + str(self.author)
    
    def get_absolute_url(self):
        return reverse('myapp:blog-detail', args=[str(self.id)])

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category_image = models.ImageField(upload_to='imgs/', default='img1.jpg')

    def __str__(self):
        return self.name
    
# Article Model
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image_url = models.URLField()
    pub_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked_articles', blank=True)

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title
    def user_has_liked(self, user):
        return self.likes.filter(id=user.id).exists()
#Comments Model
class comment(models.Model):
    news = models.ForeignKey(Article, related_name="comments", on_delete=models.CASCADE )
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)
    
class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=100)
    subject = models.TextField()

    def __str__(self):
        return f"Contact info from: {self.name}"