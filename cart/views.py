from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem, Course
from .serializers import CartSerializer, CartItemSerializer

class ViewCart(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({'detail': 'Cart not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CartSerializer(cart)
        return Response(serializer.data)

class AddToCart(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({'detail': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Get or create the user's cart
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Create a CartItem if it doesn't exist for the course
        cart_item, created = CartItem.objects.get_or_create(cart=cart, course=course)

        if not created:
            return Response({'detail': 'Course already in cart.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Item added to cart.'}, status=status.HTTP_201_CREATED)

class RemoveFromCart(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        try:
            cart_item = CartItem.objects.get(id=item_id)

        except CartItem.DoesNotExist:
            return Response({'detail': 'Cart item not found.'}, status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()
        return Response({'detail': 'Item removed from cart.'}, status=status.HTTP_204_NO_CONTENT)
