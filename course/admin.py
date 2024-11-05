from django.contrib import admin
from django_ckeditor_5.widgets import CKEditor5Widget
from django.forms import Textarea
from .models import Category, Course, CourseChapter, Section, CourseHashtag, CourseMaster, Hashtag
from master.models import Artist
from django.db import models


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class CourseChapterInline(admin.TabularInline):
    model = CourseChapter
    extra = 1
    verbose_name = "Course Chapter"
    verbose_name_plural = "Course Chapters"


class SectionInline(admin.TabularInline):
    model = Section
    extra = 1
    verbose_name = "Section"
    verbose_name_plural = "Sections"


class CourseHashtagInline(admin.TabularInline):
    model = CourseHashtag
    extra = 1
    verbose_name = "Course Hashtag"
    verbose_name_plural = "Course Hashtags"

class ArtistInline(admin.TabularInline):
    model = CourseHashtag
    extra = 1
    verbose_name = "Course Master"
    verbose_name_plural = "Course Masters"


class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'category', 'price', 'rating']
    list_filter = ['level', 'category', 'price']
    search_fields = ['name', 'category__name']
    list_editable = ['price', 'rating']
    inlines = [CourseChapterInline, SectionInline, CourseHashtagInline,ArtistInline]

    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='extends')},
    }


class HashtagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


admin.site.register(Hashtag, HashtagAdmin)
admin.site.register(Course, CourseAdmin)


class CourseMasterAdmin(admin.ModelAdmin):
    list_display = ['master', 'course']
    list_filter = ['course']
    search_fields = ['master__name', 'course__name']


admin.site.register(CourseMaster, CourseMasterAdmin)


class CourseHashtagAdmin(admin.ModelAdmin):
    list_display = ['course', 'hashtag']
    list_filter = ['course', 'hashtag']
    search_fields = ['course__name', 'hashtag__name']


admin.site.register(CourseHashtag, CourseHashtagAdmin)
