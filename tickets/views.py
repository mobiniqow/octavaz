from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Ticket, TicketCategory, TicketResponse
from .serializers import TicketSerializer, TicketResponseSerializer, TicketCategorySerializer
from rest_framework.permissions import IsAuthenticated


# جزئیات تیکت و ارسال پاسخ
class TicketCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, ):
        category = TicketCategory.objects.all()
        serializer = TicketCategorySerializer(category, many=True)
        return Response(serializer.data)


# نمایش لیست تیکت‌ها
class TicketListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tickets = Ticket.objects.all()
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # به کاربر جاری نسبت داده می‌شود
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TicketDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, ticket_id):
        # دریافت تیکت و پاسخ‌های مربوطه
        ticket = Ticket.objects.get(id=ticket_id)
        responses = TicketResponse.objects.filter(ticket=ticket).order_by('created_at')  # مرتب‌سازی پاسخ‌ها
        ticket_serializer = TicketSerializer(ticket)
        response_serializer = TicketResponseSerializer(responses, many=True)  # سریالایزر پاسخ‌ها
        return Response({
            'ticket': ticket_serializer.data,
            'responses': response_serializer.data
        })

    def post(self, request, ticket_id):
        ticket = Ticket.objects.get(id=ticket_id)

        # بررسی نوع فرستنده: اگر کاربر باشد، `sender=USER` و اگر ادمین باشد، `sender=ADMIN`
        sender_type = TicketResponse.Sender.USER  # پیش‌فرض برای کاربر
        if request.user.is_staff:  # اگر کاربر ادمین باشد
            sender_type = TicketResponse.Sender.ADMIN

        # ایجاد پاسخ جدید
        response_data = {
            'ticket': ticket.id,
            'response_text': request.data.get('response_text'),
            'response_images': request.data.get('response_images'),
            'sender': sender_type  # مشخص کردن فرستنده
        }

        response_serializer = TicketResponseSerializer(data=response_data)
        if response_serializer.is_valid():
            response_serializer.save()
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(response_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class TicketResponseView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, ticket_id):
#         ticket = Ticket.objects.get(id=ticket_id)
#         response_serializer = TicketResponseSerializer(data=request.data)
#         if response_serializer.is_valid():
#             response_serializer.save(ticket=ticket, admin_user=request.user)
#             return Response(response_serializer.data, status=status.HTTP_201_CREATED)
#         return Response(response_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
