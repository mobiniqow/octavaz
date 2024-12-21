from django.urls import path
from .views import ViewCart, AddToCart, RemoveFromCart

urlpatterns = [
    path('cart/', ViewCart.as_view(), name='view_cart'),
    path('cart/add/<int:course_id>/', AddToCart.as_view(), name='add_to_cart'),
    path('cart/remove/<int:item_id>/', RemoveFromCart.as_view(), name='remove_from_cart'),
]
