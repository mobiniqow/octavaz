# blog/models.py
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Hashtag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = CKEditor5Field('content', )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE)
    hashtags = models.ManyToManyField(Hashtag, related_name='posts')
    allow_comments = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class BannerImage(models.Model):
    post = models.ForeignKey(Post, related_name='banner_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='banner_images/')
    order = models.PositiveIntegerField(default=1)  # برای ترتیب بنرها (1، 2، 3)

    def __str__(self):
        return f"Banner image for {self.post.title}"

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    website = models.CharField(max_length=100,default="")
    email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"
