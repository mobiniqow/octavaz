from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


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
