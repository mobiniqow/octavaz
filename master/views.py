from time import timezone

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from datetime import timedelta
from course.models import CourseMaster, UserCourse, Course, CourseChapter, CourseChapterMedia
from course.serializers import CourseSerializer, CourseChapterSerializer, CourseChapterMediaSerializer, \
    CourseDetailSerializer
from train.models import Train, Feedback
from train.serializers import FeedbackSerializer
from .models import Artist, ArtistTransaction
from .serializers import ArtistSerializer, ArtistPaymentRequestSerializer, ArtistTransactionSerializers, \
    CertificateSerializer, CertificateUserSerializer
from django.db.models import Sum
from datetime import timedelta
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CourseMasterCertificate
from .serializers import CertificateCreateSerializer

class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class MasterCourseView(APIView):

    def get(self, request, **kwargs):
        course = [i.course for i in CourseMaster.objects.filter(master__master=request.user)]
        serializers = CourseSerializer(course, many=True)
        return Response(serializers.data)


class MasterTransactionView(APIView):
    def get(self, request, **kwargs):
        artists = ArtistTransaction.objects.filter(artist__master=request.user,
                                                   status=ArtistTransaction.TransactionStatus.SUCCESS)
        serializers = ArtistTransactionSerializers(artists, many=True)
        return Response(serializers.data)


class GetPriceView(APIView):

    def get(self, request, **kwargs):
        course = [i.course for i in CourseMaster.objects.filter(master__master=request.user)]
        serializers = CourseSerializer(course, many=True)
        return Response(serializers.data)


class ArtistSalesView(APIView):

    def get(self, request, **kwargs):
        user = request.user
        try:
            artist = Artist.objects.get(master=user)
        except Artist.DoesNotExist:
            return Response({"error": "No artist found for this user"}, status=404)
        one_year_ago = timezone.now() - timedelta(days=365)
        artist_transactions = ArtistTransaction.objects.filter(
            artist=artist,
            status=ArtistTransaction.TransactionStatus.SUCCESS,
            created_at__gte=one_year_ago
        )
        total_sales = artist_transactions.aggregate(total_sales=Sum('price'))['total_sales'] or 0
        courses = CourseMaster.objects.filter(master=artist)
        total_paid = 0
        for course in courses:
            user_courses = UserCourse.objects.filter(course=course.course, is_paid=True)
            for user_course in user_courses:
                if user_course.transaction.status == 'success':
                    total_paid += user_course.transaction.amount
        remaining_balance = total_sales - total_paid
        artist_info = {
            'artist_name': artist.name,
            'total_sales': total_sales,
            'total_paid': total_paid,
            'remaining_balance': remaining_balance,
        }

        return Response(artist_info)

    def post(self, request, **kwargs):
        user = request.user
        try:
            artist = Artist.objects.get(master=user)
        except Artist.DoesNotExist:
            return Response({"error": "No artist found for this user"}, status=404)

        serializer = ArtistPaymentRequestSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            description = serializer.validated_data['description']

            artist_transaction = ArtistTransaction.objects.create(
                artist=artist,
                price=amount,
                status=ArtistTransaction.TransactionStatus.REQUEST,
                created_at=timezone.now(),
                price_type=ArtistTransaction.PriceType.RIAL
            )

            return Response({
                "message": "Your payment request has been successfully submitted.",
                "transaction_id": artist_transaction.id,
                "amount": amount,
                "description": description,
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArtistTrainings(APIView):

    def get(self, request, **kwargs):
        user = request.user
        course_id = kwargs.get("id")

        if course_id:  # وقتی ID داده شده، تکالیف یک کورس خاص بازگردانده می‌شود
            trainings = Train.objects.filter(course__id=course_id)

            serialized_trainings = [
                {
                    "id": training.id,
                    "descriptions": training.descriptions,
                    "training_type": training.get_training_type_display(),
                    "media_file": training.media_file.url if training.media_file else None,
                    "master_point": training.master_point,
                }
                for training in trainings
            ]
            return Response(serialized_trainings, status=status.HTTP_200_OK)

        courses = (
            CourseMaster.objects.filter(master__master=user)
            .values("course_id", "course__name")
            .distinct()
        )

        course_stats = []
        for course in courses:
            course_id = course["course_id"]
            course_name = course["course__name"]
            student_count = Train.objects.filter(course_id=course_id).values("user").distinct().count()
            assignment_count = Train.objects.filter(course_id=course_id).count()

            course_stats.append(
                {
                    "id": course_id,
                    "name": course_name,
                    "student_count": student_count,
                    "assignment_count": assignment_count,
                }
            )

        return Response(course_stats, status=status.HTTP_200_OK)


class FeedbackView(APIView):

    def post(self, request, feedback_id):
        """
        Add feedback for a specific train.
        """
        train = Train.objects.filter(pk=feedback_id).first()
        if not train:
            return Response({"error": "Train not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            data = request.data
            data["train"] = train.id
            data["master"] = request.user.id
            serializer = FeedbackSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, feedback_id):
        """
        Update feedback.
        """
        feedback = Feedback.objects.filter(id=feedback_id, master=request.user).first()
        if not feedback:
            return Response({"error": "Feedback not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = FeedbackSerializer(feedback, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, feedback_id):
        """
        Delete feedback.
        """
        feedback = Feedback.objects.filter(id=feedback_id, master=request.user).first()
        if not feedback:
            return Response({"error": "Feedback not found"}, status=status.HTTP_404_NOT_FOUND)

        feedback.delete()
        return Response({"message": "Feedback deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# course management api
class CourseManagementView(APIView):

    def post(self, request):
        """
        Create a new course.
        """
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, course_id):
        """
        Update an existing course.
        """
        course = Course.objects.filter(id=course_id, coursemaster__master=request.user).first()
        if not course:
            return Response({"error": "Course not found or access denied."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, course_id):
        """
        Delete a course.
        """
        course = Course.objects.filter(id=course_id, coursemaster__master=request.user).first()
        if not course:
            return Response({"error": "Course not found or access denied."}, status=status.HTTP_404_NOT_FOUND)

        course.delete()
        return Response({"message": "Course deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    def get(self, request):
        """
        List all courses of the current master.
        """
        course = [i.course.id for i in CourseMaster.objects.filter(master__master=request.user)]
        courses = Course.objects.filter(id__in=course)
        serializer = CourseDetailSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# API for managing course chapters
class ChapterManagementView(APIView):

    def post(self, request, course_id):
        """
        Add a chapter to a course.
        """
        course = Course.objects.filter(id=course_id, coursemaster__master=request.user).first()
        if not course:
            return Response({"error": "Course not found or access denied."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        data['course'] = course.id
        serializer = CourseChapterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, chapter_id):
        """
        Update a course chapter.
        """
        chapter = CourseChapter.objects.filter(id=chapter_id, course__coursemaster__master=request.user).first()
        if not chapter:
            return Response({"error": "Chapter not found or access denied."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CourseChapterSerializer(chapter, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, chapter_id):
        """
        Delete a course chapter.
        """
        chapter = CourseChapter.objects.filter(id=chapter_id, course__coursemaster__master=request.user).first()
        if not chapter:
            return Response({"error": "Chapter not found or access denied."}, status=status.HTTP_404_NOT_FOUND)

        chapter.delete()
        return Response({"message": "Chapter deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


# API for managing chapter media
class ChapterMediaManagementView(APIView):
    def post(self, request, chapter_id):
        """
        Add media to a chapter.
        """
        chapter = CourseChapter.objects.filter(id=chapter_id, course__coursemaster__master=request.user).first()
        if not chapter:
            return Response({"error": "Chapter not found or access denied."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        data['course_chapter'] = chapter.id
        serializer = CourseChapterMediaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, media_id):
        """
        Delete media from a chapter.
        """
        media = CourseChapterMedia.objects.filter(id=media_id,
                                                  course_chapter__course__coursemaster__master=request.user).first()
        if not media:
            return Response({"error": "Media not found or access denied."}, status=status.HTTP_404_NOT_FOUND)

        media.delete()
        return Response({"message": "Media deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


# API for course analytics
class CourseAnalyticsView(APIView):

    def get(self, request, course_id):
        """
        Retrieve analytics for a course, including revenue, enrollment, and creation date.
        """
        course = Course.objects.filter(id=course_id, coursemaster__master=request.user).first()
        if not course:
            return Response({"error": "Course not found or access denied."}, status=status.HTTP_404_NOT_FOUND)

        # Calculate total revenue and enrollment count
        total_revenue = \
        UserCourse.objects.filter(course=course, is_paid=True).aggregate(total=Sum('transaction__amount'))['total'] or 0
        enrollment_count = UserCourse.objects.filter(course=course).count()

        data = {
            "course_name": course.name,
            "total_revenue": total_revenue,
            "enrollment_count": enrollment_count,
            "created_at": course.created_at,
        }
        return Response(data, status=status.HTTP_200_OK)


class IssueCertificateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # بررسی اینکه کاربر ادمین باشد
        if not request.user.is_staff:
            return Response({"detail": "You do not have permission to issue certificates."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = CertificateCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            certificate = serializer.save()
            return Response({"detail": "Certificate issued successfully.", "certificate_id": certificate.id},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ViewAllCertificateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request,  ):
        try:
            certificate = CourseMasterCertificate.objects.filter( issued_to=request.user)
        except CourseMasterCertificate.DoesNotExist:
            return Response({"detail": "Certificate not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CertificateUserSerializer(certificate,many=True)
        return Response(serializer.data)

class ViewCertificateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, certificate_id):
        try:
            certificate = CourseMasterCertificate.objects.get(id=certificate_id, issued_to=request.user)
        except CourseMasterCertificate.DoesNotExist:
            return Response({"detail": "Certificate not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CertificateUserSerializer(certificate)
        return Response(serializer.data)

class CertificateInfoView(APIView):

    def get(self, request, certificate_id):
        try:
            certificate = CourseMasterCertificate.objects.get(id=certificate_id)
        except CourseMasterCertificate.DoesNotExist:
            return Response({"detail": "Certificate not found."}, status=status.HTTP_404_NOT_FOUND)

        # ارسال اطلاعات بدون فایل PDF
        serializer = CertificateSerializer(certificate)
        return Response(serializer.data)
