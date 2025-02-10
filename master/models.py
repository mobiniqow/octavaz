from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.db import models
import uuid

from course.models import Course, CourseMaster


class Artist(models.Model):
    name = models.CharField(max_length=100)
    instrument = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    master = models.ForeignKey('account.User', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class ArtistTransaction(models.Model):
    class TransactionStatus(models.IntegerChoices):
        REQUEST = 0, 'Request'
        IN_PROGRESS = 1, 'InProgress'
        FAILED = 2, 'Failed'
        SUCCESS = 3, 'Success'

    class PriceType(models.IntegerChoices):
        RIAL = 0, 'Rial'
        DOLLAR = 1, 'Dollar'

    status = models.IntegerField(choices=TransactionStatus.choices, default=TransactionStatus.REQUEST)
    created_at = models.DateTimeField(auto_now_add=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    price = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(10000000)])
    price_type = models.IntegerField(choices=PriceType.choices, default=PriceType.RIAL)


class CourseMasterCertificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(CourseMaster, on_delete=models.CASCADE)
    certificate = models.FileField(upload_to='certificates/', )
    state = models.CharField(max_length=20,
                             choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
                             default='pending')
    issued_to = models.ForeignKey('account.User', on_delete=models.CASCADE,
                                  related_name='user_certificates')  # the user receiving the certificate
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Certificate for {self.course.course.name} - {self.state}"
