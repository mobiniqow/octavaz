from django.contrib import admin
from .models import (
    Category, CourseBase, Course, CourseMaster, CourseChapter,
    Section, Hashtag, CourseHashtag, CourseChapterMedia, ChapterPurchase,
    UserCourse, CourseQuestion, CourseAnswer
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(CourseBase)
class CourseBaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'level', 'category')
    list_filter = ('type', 'level', 'category')
    search_fields = ('name', 'category__name')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'level', 'category', 'price', 'rating', 'time', 'trainings')
    list_filter = ('type', 'level', 'category', 'rating')
    search_fields = ('name', 'category__name')

@admin.register(CourseMaster)
class CourseMasterAdmin(admin.ModelAdmin):
    list_display = ('id', 'master', 'course')
    search_fields = ('master__name', 'course__name')

@admin.register(CourseChapter)
class CourseChapterAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'chapter', 'name')
    search_fields = ('course__name', 'name')

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'course')
    search_fields = ('name', 'course__name')

@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(CourseHashtag)
class CourseHashtagAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'hashtag')
    search_fields = ('course__name', 'hashtag__name')

@admin.register(CourseChapterMedia)
class CourseChapterMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'course_chapter')
    search_fields = ('course_chapter__name',)

@admin.register(ChapterPurchase)
class ChapterPurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'chapter', 'is_paid', 'purchased_at')
    list_filter = ('is_paid', 'purchased_at')
    search_fields = ('user__user_name', 'chapter__name')

@admin.register(UserCourse)
class UserCourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'transaction', 'is_paid')
    list_filter = ('is_paid',)
    search_fields = ('user__user_name', 'course__name')

@admin.register(CourseQuestion)
class CourseQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'course', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('student__user_name', 'course__name', 'question_text')

@admin.register(CourseAnswer)
class CourseAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'responder', 'created_at')
    search_fields = ('question__question_text', 'responder__user_name')
