from django.db import models

from django.core.exceptions import ValidationError

class Options(models.Model):
    logo = models.ImageField(upload_to='logo/')
    intro_video = models.FileField(upload_to='intro_video/')
    intro_text = models.TextField()

    def save(self, *args, **kwargs):
        if not self.pk and Options.objects.exists():
            raise ValidationError("Only one Options instance is allowed.")
        super().save(*args, **kwargs)
