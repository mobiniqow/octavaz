from rest_framework import serializers
from .models import Train


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = "__all__"
        read_only_fields = ['can_delete', 'user', 'training_type', 'master_point']
