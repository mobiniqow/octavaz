from rest_framework import serializers
from .models import Train, Feedback


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = "__all__"
        read_only_fields = ['can_delete', 'user', 'training_type', 'master_point']

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ["id", "train", "master", "description", "master_point", "media_file", "created_at", "updated_at"]
        read_only_fields = ["master", "created_at", "updated_at"]