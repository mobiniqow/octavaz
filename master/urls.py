from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArtistViewSet, MasterCourseView, ArtistSalesView, MasterTransactionView, ArtistTrainings, \
    FeedbackView, CourseAnalyticsView, ChapterMediaManagementView, ChapterManagementView, CourseManagementView

router = DefaultRouter()
router.register(r"artists", ArtistViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("course", MasterCourseView.as_view()),
    path("price", ArtistSalesView.as_view()),
    path("transactions", MasterTransactionView.as_view()),
    path('artist-trainings/', ArtistTrainings.as_view(), name='artist-trainings-list'),
    path('artist-trainings/<int:id>/', ArtistTrainings.as_view(), name='artist-trainings-detail'),
    path('feedback/<int:feedback_id>/', FeedbackView.as_view(), name='feedback-manage'),
    path('courses/', CourseManagementView.as_view(), name='course-list-create'),
    path('courses/<int:course_id>/', CourseManagementView.as_view(), name='course-update-delete'),
    path('courses/<int:course_id>/chapters/', ChapterManagementView.as_view(), name='chapter-create'),
    path('chapters/<int:chapter_id>/', ChapterManagementView.as_view(), name='chapter-update-delete'),
    path('chapters/<int:chapter_id>/media/', ChapterMediaManagementView.as_view(), name='chapter-media-create'),
    path('media/<int:media_id>/', ChapterMediaManagementView.as_view(), name='media-delete'),
    path('courses/<int:course_id>/analytics/', CourseAnalyticsView.as_view(), name='course-analytics'),

]
