from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from account.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CourseBase(models.Model):
    class Type(models.IntegerChoices):
        NORMAL = 0
        GENERAL = 1

    class Level(models.IntegerChoices):
        Beginner = 0, "Beginner"
        Intermediate = 1, "Intermediate"
        Advanced = 2, "Advanced"
        Expert = 3, "Expert"

    type = models.IntegerField(choices=Type.choices, default=Type.NORMAL)
    level = models.IntegerField(choices=Level.choices, default=Level.Beginner)
    name = models.CharField(max_length=100)
    long_description = CKEditor5Field('long_description', config_name='extends')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    course_contacts = CKEditor5Field('course_contacts', config_name='extends')
    course_requirements = CKEditor5Field('course_requirements', config_name='extends')
    course_prerequisite = CKEditor5Field('course_prerequisite', config_name='extends')
    training_model = CKEditor5Field('training_model', config_name='extends',blank=True,null=True)
    course_achievement = CKEditor5Field('course_achievement', config_name='extends',blank=True,null=True)
class Course(models.Model):
    class Type(models.IntegerChoices):
        NORMAL = 0
        GENERAL = 1

    class Level(models.IntegerChoices):
        Beginner = 0, "Beginner"
        Intermediate = 1, "Intermediate"
        Advanced = 2, "Advanced"
        Expert = 3, "Expert"

    base = models.ForeignKey('CourseBase', on_delete=models.SET_NULL,null=True,blank=True)
    type = models.IntegerField(choices=Type.choices, default=Type.NORMAL)
    level = models.IntegerField(choices=Level.choices, default=Level.Beginner)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    image = models.ImageField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = CKEditor5Field('description', config_name='extends')
    long_description = CKEditor5Field('long_description', config_name='extends')
    time = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10000)])
    trainings = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10000)])
    course_contacts = CKEditor5Field('course_contacts', config_name='extends')
    course_requirements = CKEditor5Field('course_requirements', config_name='extends')
    course_prerequisite = CKEditor5Field('course_prerequisite', config_name='extends')
    training_model = CKEditor5Field('training_model', config_name='extends')
    course_achievement = CKEditor5Field('course_achievement', config_name='extends')


class CourseMaster(models.Model):
    master = models.ForeignKey('master.Artist', on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True)

class CourseChapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    chapter = models.IntegerField()
    name = models.CharField(max_length=100)
    media = models.FileField(upload_to='media/', null=True, blank=True)

class Section(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    chapters = models.ForeignKey(CourseChapter, on_delete=models.CASCADE)


class Hashtag(models.Model):
    name = models.CharField(max_length=100)


class CourseHashtag(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)


class CourseChapterMedia(models.Model):
    order = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4000)])
    media = models.FileField(upload_to='media/')
    course_chapter = models.ForeignKey(CourseChapter, on_delete=models.CASCADE)


class ChapterPurchase(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    chapter = models.ForeignKey(CourseChapter, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.user_name} purchased {self.chapter.name}"

class UserCourse(models.Model):
    user = models.ForeignKey('account.User',on_delete=models.CASCADE,related_name='user_course',null=True,blank=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='user_course',null=True,blank=True)
    transaction = models.ForeignKey('wallet.Transaction',on_delete=models.CASCADE,related_name='user_course',null=True,blank=True)
    is_paid = models.BooleanField(default=False)

# master social

class CourseQuestion(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('ANSWERED', 'Answered'),
        ('CLOSED', 'Closed'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OPEN')

    def __str__(self):
        return f"Question by {self.student.user_name} in {self.course.name}"


class CourseAnswer(models.Model):
    question = models.ForeignKey(CourseQuestion, on_delete=models.CASCADE, related_name='answers')
    responder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer by {self.responder.user_name} for Question {self.question.id}"