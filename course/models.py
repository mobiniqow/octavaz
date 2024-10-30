from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    image = models.ImageField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    artist = models.ForeignKey('Artist', on_delete=models.SET_NULL, null=True)


class CourseChapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    chapter = models.IntegerField()
    name = models.CharField(max_length=100)


class Section(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    chapters = models.ForeignKey(CourseChapter, on_delete=models.CASCADE)
