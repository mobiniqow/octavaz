from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, CourseViewSet, CourseChapterViewSet, SectionViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"courses", CourseViewSet)
router.register(r"course-chapters", CourseChapterViewSet)
router.register(r"sections", SectionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
