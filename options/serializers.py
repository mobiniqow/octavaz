from rest_framework import serializers
from .models import Options

class OptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Options
        fields = ['id', 'logo', 'intro_video', 'intro_text']
