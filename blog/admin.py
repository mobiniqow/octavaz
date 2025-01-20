# blog/admin.py
from django.contrib import admin
from .models import Post, Category, Hashtag, Comment, BannerImage

# 1. تعریف Inline برای بنرها
class BannerImageInline(admin.TabularInline):  # می‌توانید از StackedInline هم استفاده کنید
    model = BannerImage
    extra = 1  # تعداد فرم‌های اضافی که برای اضافه کردن بنر به صورت پیش‌فرض نمایش داده می‌شود.
    fields = ('image', 'order')  # فیلدهایی که می‌خواهیم نمایش داده شوند.
    #readonly_fields = ('image',)  # فقط برای نمایش، برای ویرایش باید گزینه 'image' را بردارید.
    ordering = ('order',)  # مرتب‌سازی بر اساس فیلد 'order'

# 2. تعریف کلاس‌های مربوط به Category و Hashtag برای لیست تمیز و مناسب
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # نمایش فقط نام دسته‌بندی‌ها در لیست
    search_fields = ('name',)  # امکان جستجو بر اساس نام
    ordering = ('name',)  # مرتب‌سازی بر اساس نام دسته‌بندی‌ها

class HashtagAdmin(admin.ModelAdmin):
    list_display = ('name',)  # نمایش فقط نام هشتگ‌ها در لیست
    search_fields = ('name',)  # امکان جستجو بر اساس نام
    ordering = ('name',)  # مرتب‌سازی بر اساس نام هشتگ‌ها

# 3. تعریف کلاس ادمین برای پست‌ها
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'updated_at', 'allow_comments')  # نمایش اطلاعات کلی پست‌ها
    list_filter = ('category', 'created_at', 'allow_comments')  # فیلتر کردن بر اساس دسته‌بندی و وضعیت کامنت‌ها
    search_fields = ('title', 'content')  # امکان جستجو بر اساس عنوان و محتوای پست
    ordering = ('-created_at',)  # مرتب‌سازی بر اساس تاریخ ایجاد
    inlines = [BannerImageInline]  # استفاده از Inline برای نمایش تصاویر بنر

# 4. کلاس‌های ادمین برای کامنت‌ها
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created_at')  # نمایش اطلاعات کامنت‌ها
    list_filter = ('created_at', 'post')  # فیلتر کردن کامنت‌ها بر اساس تاریخ و پست
    search_fields = ('name', 'content', 'post__title')  # جستجو بر اساس نام، محتوا و عنوان پست
    ordering = ('-created_at',)  # مرتب‌سازی بر اساس تاریخ ایجاد

# ثبت مدل‌ها و کلاس‌های ادمین در پنل ادمین
admin.site.register(Category, CategoryAdmin)
admin.site.register(Hashtag, HashtagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
