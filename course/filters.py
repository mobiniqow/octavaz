from django_filters import rest_framework as filters
from .models import Course

class CourseFilter(filters.FilterSet):
    category = filters.NumberFilter(field_name='category', lookup_expr='exact')  # فیلتر بر اساس ID کتگوری

    class Meta:
        model = Course
        fields = ['category']

