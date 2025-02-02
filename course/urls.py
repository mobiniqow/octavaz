from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, CourseViewSet, CourseChapterViewSet, SectionViewSet, PurchasedCoursesView, \
    CourseBaseDetailView, \
    StudentReport, StudentCourse, CourseBaseViewSet, CourseQuestionView, CourseAnswerView, CourseAllQuestionsView

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"courses", CourseViewSet)
router.register(r"course-chapters", CourseChapterViewSet)
router.register(r"base-course", CourseBaseViewSet)
router.register(r"sections", SectionViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path('purchased-courses/', PurchasedCoursesView.as_view(), name='purchased-courses'),
    path('user-details/', StudentReport.as_view(), name='user-details'),
    # path('base-course',CourseBaseDetailView.as_view(), name='base-course'),
    path('user-course',StudentCourse.as_view(), name='base-course'),
    path('api/courses/<int:course_id>/questions/', CourseQuestionView.as_view(), name='course-questions'),
    path('api/questions/<int:question_id>/answers/', CourseAnswerView.as_view(), name='course-answers'),
    path('api/questions/', CourseAllQuestionsView.as_view(), name='course-all-question'),
]
