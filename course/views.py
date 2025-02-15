from django.db.transaction import atomic
from rest_framework import viewsets, status
from rest_framework import filters

from tickets.models import TicketResponse
from wallet.models import Transaction
from .models import Category, Course, CourseChapter, Section, UserCourse, CourseBase, CourseQuestion, CourseMaster, \
    CourseAnswer
from .serializers import SerializerCategorySerializer, CourseSerializer, CourseChapterSerializer, SectionSerializer, \
    CourseBaseSerializer, CourseQuestionSerializer, CourseAnswerSerializer
from .filters import CourseFilter, BaseCourseFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ChapterPurchase, CourseChapter
from .serializers import ChapterPurchaseSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = SerializerCategorySerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = CourseFilter
    # search_fields = ['category__name']


class CourseBaseViewSet(viewsets.ModelViewSet):
    queryset = CourseBase.objects.all()
    serializer_class = CourseBaseSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = BaseCourseFilter
#

class CourseChapterViewSet(viewsets.ModelViewSet):
    queryset = CourseChapter.objects.all()
    serializer_class = CourseChapterSerializer


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer


class PurchasedCoursesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        purchases = ChapterPurchase.objects.filter(user=user, is_paid=True).select_related('chapter__course')

        # آماده‌سازی داده‌ها برای پاسخ
        data = [
            {
                "course_name": purchase.chapter.course.name,
                "chapter_name": purchase.chapter.name,
                "purchased_at": purchase.purchased_at,
                "payment_method": purchase.payment_method,
            }
            for purchase in purchases
        ]

        return Response(data)

class CourseBaseDetailView(APIView):
    def get(self, request):
        course_base = CourseBase.objects.all()
        serializer = CourseBaseSerializer(course_base,many=True)
        return Response(serializer.data)

class StudentReport(APIView):
    def get(self, request, **kwargs):
        return Response({
            "messages_count": TicketResponse.objects.filter(ticket__user=request.user,
                                                            state=TicketResponse.ResponseState.UNREAD).count(),
            "course_count":UserCourse.objects.filter(user=request.user).count(),
            "transaction_count":Transaction.objects.filter(user=request.user).count()
        })

class StudentCourse(APIView):

    def get(self,request,**kwargs):
        user_courses = [i.course for i in UserCourse.objects.filter(user=request.user)]
        serializer = CourseSerializer(user_courses,many=True)
        return Response(serializer.data)

class CourseQuestionView(APIView):
    permission_classes = [IsAuthenticated]

    @atomic
    def post(self, request, course_id):
        """
        Submit a new question for a course.
        """
        # ایجاد یک نسخه قابل تغییر از داده‌های ارسال شده

        try:
            student = request.user
            course = Course.objects.filter(id=course_id).first()
            question_text = request.data.get('question_text')
            CourseQuestion.objects.create(student=student, course=course, question_text=question_text)
            return Response({"message": "Question submitted successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, course_id):
        """
        Get all questions and answers for a course.
        """
        questions = CourseQuestion.objects.filter(course_id=course_id).prefetch_related('answers')
        serializer = CourseQuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseAnswerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, question_id):
        """
        Add an answer to a specific question.
        """
        question = CourseQuestion.objects.filter(id=question_id).first()
        if not question:
            return Response({"error": "Question not found"}, status=status.HTTP_404_NOT_FOUND)

        data_req = request.data
        data = {}
        data['question'] = question.id
        data['responder'] = request.user.id
        data['answer_text'] = data_req.get('answer_text')
        serializer = CourseAnswerSerializer(data=data)
        if serializer.is_valid():
            question.status = 'ANSWERED'
            CourseAnswer.objects.create(**serializer.validated_data,responder=request.user)
            question.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseAllQuestionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request,):
        courses = [i.course.id for i in CourseMaster.objects.filter(master__master=request.user)]
        question = CourseQuestion.objects.filter(course_id__in=courses)
        serializers = CourseQuestionSerializer(question,many=True)
        return Response(serializers.data)
