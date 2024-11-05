from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Course(models.Model):
    class Level(models.IntegerChoices):
        Beginner = 0, "Beginner"
        Intermediate = 1, "Intermediate"
        Advanced = 2, "Advanced"
        Expert = 3, "Expert"

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


class Section(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    chapters = models.ForeignKey(CourseChapter, on_delete=models.CASCADE)


class Hashtag(models.Model):
    name = models.CharField(max_length=100)


class CourseHashtag(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)
