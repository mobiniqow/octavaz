from rest_framework import serializers
from .models import Category, Course, CourseChapter, Section


class CategorySerializer(serializers.ModelSerializer):
    season =serializers.SerializerMethodField()
    lesson = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = "__all__"

    def get_season(self, obj):
        return obj.season


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseChapter
        fields = "__all__"


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = "__all__"
