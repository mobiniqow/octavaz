from django.contrib import admin
from .models import Category, CourseBase, Course, CourseMaster, CourseChapter, Section, Hashtag, CourseHashtag, CourseChapterMedia, ChapterPurchase


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class CourseAdminInLine(admin.TabularInline):
    model = Course


class CourseBaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'level', 'category')
    list_filter = ('type', 'level', 'category')
    search_fields = ('name',)
    inlines = (CourseAdminInLine,)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'level', 'category', 'price', 'rating', 'time', 'trainings')
    list_filter = ('type', 'level', 'category')
    search_fields = ('name', 'category__name')

class CourseMasterAdmin(admin.ModelAdmin):
    list_display = ('master', 'course')
    search_fields = ('master__name', 'course__name')


class CourseChapterAdmin(admin.ModelAdmin):
    list_display = ('course', 'chapter', 'name')
    list_filter = ('course',)
    search_fields = ('name',)


class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'course')
    list_filter = ('course',)
    search_fields = ('name',)


class HashtagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class CourseHashtagAdmin(admin.ModelAdmin):
    list_display = ('course', 'hashtag')
    list_filter = ('course', 'hashtag')


class CourseChapterMediaAdmin(admin.ModelAdmin):
    list_display = ('order', 'media', 'course_chapter')
    list_filter = ('course_chapter',)
    search_fields = ('course_chapter__name',)


class ChapterPurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'chapter', 'purchased_at', 'is_paid', 'payment_method')
    list_filter = ('is_paid', 'payment_method')
    search_fields = ('user__user_name', 'chapter__name')


admin.site.register(Category, CategoryAdmin)
admin.site.register(CourseBase, CourseBaseAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseMaster, CourseMasterAdmin)
admin.site.register(CourseChapter, CourseChapterAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Hashtag, HashtagAdmin)
admin.site.register(CourseHashtag, CourseHashtagAdmin)
admin.site.register(CourseChapterMedia, CourseChapterMediaAdmin)
admin.site.register(ChapterPurchase, ChapterPurchaseAdmin)
