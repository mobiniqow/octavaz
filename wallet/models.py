from django.db import models
from django.conf import settings
from django.utils import timezone
import requests
from cart.models import Cart, CartItem

import json

from course.models import Course


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
    ]

    TRANSACTION_STATUS = [
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ]

    user = models.ForeignKey("account.User", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    status = models.CharField(max_length=10, choices=TRANSACTION_STATUS, default='pending')
    timestamp = models.DateTimeField(default=timezone.now)
    authority = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Transaction {self.transaction_type} - {self.amount} - {self.status}"

    def save(self, *args, **kwargs):
        if self.transaction_type == 'deposit' and self.status == 'success':
            # پرداخت موفق
            cart = Cart.objects.filter(user=self.user).first()
            for i in CartItem.objects.filter(cart=cart):
                CourseIncoming.objects.create(course=i.course, price=i.course.price,user=i.cart.user)

            if cart:
                cart.items.all().delete()
        super().save(*args, **kwargs)


class Payment(models.Model):
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE)
    payment_url = models.URLField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('completed', 'Completed'),
                                                      ('failed', 'Failed')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.cart.user.user_name} - {self.status}"

    def initiate_payment(self):
        # Logic to start the payment using Zarinpal API
        amount = self.cart.total_amount()
        if amount <= 0:
            raise ValueError("سبد خرید خالی است یا مبلغ پرداخت صحیح نیست.")

        url = "https://api.zarinpal.com/pg/v4/payment/request.json"
        data = {
            'merchant_id': settings.MERCHANT_ID,
            'amount': str(amount),
            'callback_url': settings.CALLBACK_URL,
            'description': f"پرداخت برای سبد خرید {self.user.user_name}",
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            response_data = json.loads(response.text)
            if response_data['data']['code'] == 100:
                self.payment_url = response_data['data']
                transaction = self.transaction
                transaction.authority = response_data['data']['authority']
                transaction.save()
                self.status = 'pending'
                self.save()
                return self.payment_url
            else:
                self.status = 'failed'
                self.save()
                raise Exception(f"خطا در درخواست پرداخت: {response_data['data']['message']}")
        else:
            self.status = 'failed'
            self.save()
            raise Exception("خطا در ارتباط با زرین‌پال")


class CourseIncoming(models.Model):
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    price = models.IntegerField(default=0, )
    user = models.ForeignKey("account.User", on_delete=models.CASCADE, null=True, blank=True)