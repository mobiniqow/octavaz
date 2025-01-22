from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from course.models import CourseChapter, ChapterPurchase
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

    def post(self, request, course_ids):
        # تبدیل رشته شناسه‌ها به لیست
        course_ids = course_ids.split(',')

        # بررسی وجود حداقل یک شناسه معتبر
        if not course_ids:
            return Response({'detail': 'No course IDs provided.'}, status=status.HTTP_400_BAD_REQUEST)

        # دریافت یا ساخت سبد خرید کاربر
        cart, _ = Cart.objects.get_or_create(user=request.user)

        added_courses = []
        already_in_cart = []
        not_found_courses = []

        # پردازش هر شناسه کورس
        for course_id in course_ids:
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                not_found_courses.append(course_id)
                continue

            # بررسی یا ساخت آیتم سبد خرید
            cart_item, created = CartItem.objects.get_or_create(cart=cart, course=course)

            if created:
                added_courses.append(course_id)
            else:
                already_in_cart.append(course_id)

        response_data = {
            'added_courses': added_courses,
            'already_in_cart': already_in_cart,
            'not_found_courses': not_found_courses
        }

        return Response(response_data, status=status.HTTP_200_OK)

class RemoveFromCart(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        try:
            cart_item = CartItem.objects.get(id=item_id)

        except CartItem.DoesNotExist:
            return Response({'detail': 'Cart item not found.'}, status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()
        return Response({'detail': 'Item removed from cart.'}, status=status.HTTP_204_NO_CONTENT)

class AddChapterToCart(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, chapter_id):
        try:
            chapter = CourseChapter.objects.get(id=chapter_id)
        except CourseChapter.DoesNotExist:
            return Response({'detail': 'Chapter not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Get or create the user's cart
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Create a CartItem if it doesn't exist for the chapter
        cart_item, created = CartItem.objects.get_or_create(cart=cart, course_chapter=chapter)

        if not created:
            return Response({'detail': 'Chapter already in cart.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Chapter added to cart.'}, status=status.HTTP_201_CREATED)
class PurchaseChapter(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, item_id):
        try:
            cart_item = CartItem.objects.get(id=item_id)
        except CartItem.DoesNotExist:
            return Response({'detail': 'Cart item not found.'}, status=status.HTTP_404_NOT_FOUND)

        if cart_item.course_chapter:
            # خرید فصل
            chapter_purchase = ChapterPurchase.objects.create(
                user=request.user,
                chapter=cart_item.course_chapter,
                is_paid=True,  # فرض کنید که در این مرحله پرداخت انجام شده
            )
            cart_item.delete()  # حذف از سبد خرید بعد از خرید
            return Response({'detail': 'Chapter purchased successfully.'}, status=status.HTTP_201_CREATED)
        return Response({'detail': 'Invalid item type in cart.'}, status=status.HTTP_400_BAD_REQUEST)
