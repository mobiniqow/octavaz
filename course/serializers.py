from django.shortcuts import get_object_or_404
from rest_framework import serializers

from cart.models import CartItem
from wallet.models import Payment, CourseIncoming
from .models import Category, Course, CourseChapter, Section, ChapterPurchase, CourseBase, CourseAnswer, CourseQuestion, \
    CourseChapterMedia, CourseMaster, UserCourse


class SerializerCategorySerializer(serializers.ModelSerializer):
    # season =serializers.SerializerMethodField()
    # lesson = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = "__all__"

    # def get_season(self, obj):
    #     return obj.season
    ref_name = 'CourseCategorySerializer'


class CourseChapterMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseChapterMedia
        fields = ['id', 'order', 'media', 'course_chapter']


class CourseChapterSerializer(serializers.ModelSerializer):
    medias = CourseChapterMediaSerializer(source='coursechaptermedia_set', many=True, read_only=True)

    class Meta:
        model = CourseChapter
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    chapters = serializers.SerializerMethodField()
    artist = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()
    income_price = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'name', 'description', 'long_description', 'price', 'image',
            'category', 'level', 'type', 'time', 'trainings', 'course_contacts',
            'course_requirements', 'course_prerequisite', 'training_model',
            'course_achievement', 'chapters', 'created_at','artist','customer','income_price',
        ]

    def get_chapters(self, obj):
        chapters = CourseChapter.objects.filter(course=obj)
        return CourseChapterSerializer(chapters, many=True).data

    def get_artist(self, obj):
        try:
            return CourseMaster.objects.filter(course=obj).first().master.master.user_name
        except Exception as _:
            return ""

    def get_customer(self, obj):
        return UserCourse.objects.filter(course=obj).count()

    def get_income_price(self, obj):
        return sum([i.price for i in CourseIncoming.objects.filter(course=obj)])


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
    category = SerializerCategorySerializer(read_only=True)
    coursechapters = CourseChapterSerializer(source='coursechapter_set', many=True, read_only=True)
    courses = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    masters = serializers.SerializerMethodField()  # فیلد برای نمایش اساتید

    class Meta:
        model = CourseBase
        fields = '__all__'

    def get_total_price(self, obj):
        total_price = 0
        for course in obj.course_set.all():
            total_price += course.price
        return total_price

    def get_courses(self, obj):
        courses = Course.objects.filter(base=obj)
        return CourseSerializer(courses, many=True).data

    def get_masters(self, obj):
        # استخراج اساتید مرتبط با دوره‌ها
        masters = CourseMaster.objects.filter(course__base=obj)
        return CourseMasterSerializer(masters, many=True).data


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
    artist = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()
    income_price = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'name', 'description', 'long_description', 'price', 'image',
            'category', 'level', 'type', 'time', 'trainings', 'course_contacts',
            'course_requirements', 'course_prerequisite', 'training_model',
            'course_achievement', 'chapters','artist','customer','income_price',
        ]

    def get_chapters(self, obj):
        chapters = CourseChapter.objects.filter(course=obj)
        return CourseChapterSerializer(chapters, many=True).data


    def get_artist(self, obj):
        try:
            return CourseMaster.objects.filter(course=obj).first().master.master.user_name
        except Exception as _:
            return ""

    def get_customer(self, obj):
        return UserCourse.objects.filter(course=obj).count()

    def get_income_price(self, obj):
        return sum([i.price for i in CourseIncoming.objects.filter(course=obj)])
class CourseMasterSerializer(serializers.ModelSerializer):
    master_name = serializers.CharField(source='master.name', read_only=True)

    class Meta:
        model = CourseMaster
        fields = ['master', 'master_name']
