from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=100)
    instrument = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/',blank=True,null=True)
    def __str__(self):
        return self.name
