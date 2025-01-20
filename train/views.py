from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Train, Feedback
from .serializers import TrainSerializer, FeedbackSerializer
from django.shortcuts import get_object_or_404


class TrainListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # فیلتر کردن تمرینات براساس کاربر فعلی
        trains = Train.objects.filter(user=request.user)
        serializer = TrainSerializer(trains, many=True)
        return Response(serializer.data)

    def post(self, request):
        # ایجاد یک تمرین جدید و اختصاص آن به کاربر فعلی
        serializer = TrainSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # اختصاص تمرین به کاربر فعلی
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TrainDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        # پیدا کردن تمرین فقط برای کاربر فعلی
        train = get_object_or_404(Train, pk=pk, user=request.user)
        serializer = TrainSerializer(train)
        return Response(serializer.data)

    def delete(self, request, pk):
        # پیدا کردن تمرین فقط برای کاربر فعلی و بررسی اینکه آیا can_delete=True است
        train = get_object_or_404(Train, pk=pk, user=request.user)

        # اگر can_delete برابر با False باشد، حذف انجام نشود
        if not train.can_delete:
            return Response({"detail": "This train cannot be deleted."}, status=status.HTTP_400_BAD_REQUEST)

        # حذف تمرین
        train.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

