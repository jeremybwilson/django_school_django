from __future__ import unicode_literals

from django.db import models
from ..users.models import User

# Create your models here.
class CourseManager(models.Manager):
    def validate_and_create_course(self, form_data):
        errors = []
        name = form_data['name']
        # teacher = form_data['teacher']

        if len(name) < 3:
            errors.append('Name of course must be at least 3 characters.')
        try:
            teacher = User.objects.get(id=form_data['teacher'])
            if teacher.permission_level != 'TEACHER':
                errors.append("Selected teacher invalid.")
        except:
            errors.append("Selected teacher invalid.")

        if errors:
            return (False, errors)
        else:
            course = Course.objects.create(name=name, teacher=teacher)
            return (True, course)

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=255)
    teacher = models.ForeignKey(User, related_name="courses_taught")
    students = models.ManyToManyField(User, related_name="enrolled_courses")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CourseManager()

    def __str__(self):
        return self.name