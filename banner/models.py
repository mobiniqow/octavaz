from django.db import models

# Create your models here.

class Banner(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField()
    url = models.TextField(null=True, blank=True)
