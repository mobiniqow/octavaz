from rest_framework import serializers
from .models import CourseIncoming

class CourseIncomingSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    class Meta:
        model = CourseIncoming
        fields = "__all__"

    def get_username(self, obj):
        return obj.user.user_name if obj.user else None