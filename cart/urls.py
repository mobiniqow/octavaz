from django.urls import path
from .views import ViewCart, AddToCart, RemoveFromCart, AddChapterToCart, PurchaseChapter

urlpatterns = [
    path('cart/', ViewCart.as_view(), name='view_cart'),
    path('cart/add/<str:course_ids>/', AddToCart.as_view(), name='add_to_cart'),
    path('cart/remove/<int:item_id>/', RemoveFromCart.as_view(), name='remove_from_cart'),
    path('cart/add/chapter/<int:chapter_id>/', AddChapterToCart.as_view(), name='add_chapter_to_cart'),
    path('cart/purchase/chapter/<int:item_id>/', PurchaseChapter.as_view(), name='purchase_chapter'),
]
