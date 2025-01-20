from django.db import models

from account.models import User


class VideoCast(models.Model):
    media = models.FileField(upload_to='media/', null=True, blank=True)  # Video file
    url = models.URLField(max_length=200, null=True, blank=True)  # External video URL (either URL or media should be provided)
    description = models.TextField()
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, max_length=255)  # For better referencing in URLs

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(VideoCast, related_name="comments", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.user_name} on {self.video.title}"
