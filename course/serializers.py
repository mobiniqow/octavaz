from rest_framework import serializers
from .models import Category, Course, CourseChapter, Section, ChapterPurchase, CourseBase, CourseAnswer, CourseQuestion, \
    CourseChapterMedia


class CategorySerializer(serializers.ModelSerializer):
    # season =serializers.SerializerMethodField()
    # lesson = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = "__all__"

    # def get_season(self, obj):
    #     return obj.season


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

class ChapterPurchaseSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='chapter.course.name', read_only=True)
    chapter_name = serializers.CharField(source='chapter.name', read_only=True)

    class Meta:
        model = ChapterPurchase
        fields = ['course_name', 'chapter_name', 'purchased_at', 'payment_method']

class CourseBaseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    coursechapters = CourseChapterSerializer(source='coursechapter_set', many=True, read_only=True)
    courses = serializers.SerializerMethodField()
    # محاسبه قیمت کل دوره‌ها
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CourseBase
        fields = '__all__'

    def get_total_price(self, obj):
        # محاسبه قیمت کل بر اساس فیلدهای مرتبط
        total_price = 0
        for course in obj.course_set.all():
            total_price += course.price
        return total_price
    def get_courses(self, obj):
        courses = Course.objects.filter(base=obj)
        return CourseSerializer(courses, many=True).data

class CourseAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseAnswer
        fields = ['id', 'question', 'responder', 'answer_text', 'created_at']
        read_only_fields = ['id', 'created_at', 'responder']


class CourseQuestionSerializer(serializers.ModelSerializer):
    answers = CourseAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = CourseQuestion
        fields = ['id', 'student', 'course', 'question_text', 'created_at', 'updated_at', 'status', 'answers']
        read_only_fields = ['id', 'created_at', 'updated_at', 'answers', 'student']

class CourseDetailSerializer(serializers.ModelSerializer):
    chapters = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'name', 'description', 'long_description', 'price', 'image',
            'category', 'level', 'type', 'time', 'trainings', 'course_contacts',
            'course_requirements', 'course_prerequisite', 'training_model',
            'course_achievement', 'chapters'
        ]

    def get_chapters(self, obj):
        chapters = CourseChapter.objects.filter(course=obj)
        return CourseChapterSerializer(chapters, many=True).data


class CourseChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseChapter
        fields = ['id', 'name', 'chapter', 'media']

class CourseChapterMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseChapterMedia
        fields = ['id', 'order', 'media', 'course_chapter']