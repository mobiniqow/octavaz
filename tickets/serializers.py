from rest_framework import serializers
from .models import Ticket, TicketCategory, TicketResponse


# سریالایزر برای مدل TicketCategory
class TicketCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketCategory
        fields = ['id', 'name', 'description']


# سریالایزر برای مدل Ticket
class TicketSerializer(serializers.ModelSerializer):
    # category = TicketCategorySerializer()

    class Meta:
        model = Ticket
        fields = ['id', 'title', 'description', 'category',  'created_at', 'is_resolved', 'images']



class TicketResponseSerializer(serializers.ModelSerializer):
    # sender = serializers.CharField(source='get_sender_display')

    class Meta:
        model = TicketResponse
        fields = ['id', 'ticket', 'response_text', 'response_images', 'created_at', 'state', 'sender']