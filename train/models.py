from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from account.models import User
from course.models import Section


class Train(models.Model):
    class TrainType(models.IntegerChoices):
        SUSPEND = 1
        FAILED = 2
        ACCEPTED = 3
        IN_PROGRESS = 4
        COMPLETED = 5
    can_delete= models.BooleanField(default=True)
    descriptions = models.TextField()
    course_section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    training_type = models.IntegerField(choices=TrainType.choices, default=TrainType.SUSPEND)
    media_file = models.FileField(upload_to='media/', null=True, blank=True)


class Feedback(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name="feedbacks")
    master = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feedbacks")
    description = models.TextField(null=True, blank=True)
    master_point = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    media_file = models.FileField(upload_to="media/feedbacks/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback by {self.master} for Train {self.train.id}"