from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category_image = models.ImageField(upload_to='imgs/', default='img1.jpg')

    def __str__(self):
        return self.name
    
# Article Model
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    # image = models.ImageField(upload_to='imgs/',default='img1.jpg' )
    image_url = models.URLField()
    pub_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
#Comments Model
class comment(models.Model):
    news = models.ForeignKey(Article,on_delete=models.CASCADE )
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    comment = models.TextField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.comment
    
class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=100)
    subject = models.TextField()

    def __str__(self):
        return f"Contact info from: {self.name}"