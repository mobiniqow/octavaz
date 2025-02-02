from rest_framework import serializers
from .models import Train, Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ["id", "train", "master", "description", "master_point", "media_file", "created_at", "updated_at"]
        read_only_fields = [ "created_at", "updated_at"]

class TrainSerializer(serializers.ModelSerializer):
    feedbacks = serializers.SerializerMethodField()

    class Meta:
        model = Train
        fields = "__all__"
        read_only_fields = ['can_delete', 'user', 'training_type', 'master_point']

    def get_feedbacks(self, obj):
        feedbacks = Feedback.objects.filter(train=obj)
        return FeedbackSerializer(feedbacks, many=True).data  # سریالایز کردن فیدبک‌ها


class TrainRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = ['descriptions', 'course', 'media_file', 'user']
        extra_kwargs = {
            'user': {'read_only': True}  # کاربر فقط خواندنی باشد و توسط سیستم ست شود
        }

    def create(self, validated_data):
        # کاربر فعلی را به داده‌های تایید شده اضافه می‌کنیم
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)

