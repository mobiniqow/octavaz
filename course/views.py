from rest_framework import viewsets
from rest_framework import filters
from .models import Category, Course, CourseChapter, Section
from .serializers import CategorySerializer, CourseSerializer, CourseChapterSerializer, SectionSerializer
from .filters import CourseFilter
from django_filters.rest_framework import DjangoFilterBackend

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = CourseFilter
    # search_fields = ['category__name']
#

class CourseChapterViewSet(viewsets.ModelViewSet):
    queryset = CourseChapter.objects.all()
    serializer_class = CourseChapterSerializer


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
