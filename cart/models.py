from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from course.models import Course  # فرض بر این است که مدل Course در اپ شما وجود دارد


class Cart(models.Model):
    user = models.OneToOneField("account.User", on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.user_name}"

    def total_amount(self):
        return sum(item.course.price for item in self.items.select_related('course'))


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course.name} in {self.cart.user.user_name}'s cart"


@receiver(post_save, sender=User)
def create_cart_for_user(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)
