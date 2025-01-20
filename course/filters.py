from django_filters import rest_framework as filters
from .models import Course, CourseChapter, CourseBase


class CourseFilter(filters.FilterSet):
    category = filters.NumberFilter(field_name='category', lookup_expr='exact')  # فیلتر بر اساس ID کتگوری

    class Meta:
        model = Course
        fields = ['category']


class CourseChapterFilter(filters.FilterSet):
    course = filters.NumberFilter(field_name='course', lookup_expr='exact')

    class Meta:
        model = CourseChapter
        fields = ['course']

class BaseCourseFilter(filters.FilterSet):
    category = filters.NumberFilter(field_name='category', lookup_expr='exact')  # فیلتر بر اساس ID کتگوری

    class Meta:
        model = CourseBase
        fields = ['category']
