from django.db import models

# Create your models here.
from django.db import models
from account.models import User


class TicketCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Ticket(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(TicketCategory, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    images = models.ImageField(upload_to='ticket_images/', null=True, blank=True)

    def __str__(self):
        return self.title

class TicketResponse(models.Model):
    class ResponseState(models.IntegerChoices):
        UNREAD = 0, 'Unread'
        READ = 1, 'Read'

    class Sender(models.IntegerChoices):
        USER = 1, 'User'
        ADMIN = 2, 'Admin'

    ticket = models.ForeignKey(Ticket, related_name='responses', on_delete=models.CASCADE)
    response_text = models.TextField()
    response_images = models.ImageField(upload_to='response_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(choices=ResponseState.choices, default=ResponseState.UNREAD)
    sender = models.IntegerField(choices=Sender.choices, default=Sender.USER)  # مشخص می‌کند که پیام از طرف کاربر است یا ادمین
    reply_to = models.ForeignKey("self", related_name='reply', on_delete=models.CASCADE,null=True,)
    def __str__(self):
        return f"Response to {self.ticket.title}"
