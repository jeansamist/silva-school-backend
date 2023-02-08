from django.db import models
from .functions import random_filename
from django.contrib.auth.models import Permission
# Create your models here.

from pathlib import Path
import datetime


def school_image_upload_path(instance, filename):
  ext = Path(filename).suffix
  return 'images/schools/{filename}'.format(filename=random_filename(ext))


class TimespamtedModel(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    abstract = True


class School(TimespamtedModel):
  name = models.CharField(max_length=255)
  location = models.CharField(max_length=255)
  image = models.ImageField(
      upload_to=school_image_upload_path, blank=True, null=True)


class Permission(TimespamtedModel):
  name = models.CharField(max_length=255)
  action_name = models.CharField(max_length=255)


class Role(TimespamtedModel):
  name = models.CharField(max_length=255)
  permissions = models.ManyToManyField(
      Permission, related_name="roles")


class Person(TimespamtedModel):
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  birthdate = models.DateField(default=datetime.date(2000, 10, 19))
  address = models.CharField(max_length=255, null=True, blank=True)
  sex = models.CharField(max_length=255, default='M')
  status = models.CharField(max_length=255, default='new')
  email = models.EmailField(null=True, blank=True)
  phone = models.IntegerField(null=True, blank=True)
  # avatar = models.ImageField(upload_to=upload_to2, blank=True, null=True)

  class Meta:
    abstract = True


class User(Person):
  username = models.CharField(max_length=150, unique=True, help_text=(
      "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."), error_messages={"unique": ("A user with that username already exists."), })
  password = models.TextField()
  role = models.ForeignKey(Role, related_name="users",
                           on_delete=models.CASCADE)
  schools = models.ManyToManyField(School, related_name="users")
  REQUIRED_FIELDS = ["username", "password"]


class Subject(TimespamtedModel):
  name = models.CharField(max_length=255)
  coef = models.IntegerField(default=1)
  # classes = models.ManyToManyField(Class, related_name='subjects')


class Class(TimespamtedModel):
  name = models.CharField(max_length=25)
  school = models.ForeignKey(
      School, related_name='classes', on_delete=models.CASCADE)
  subjects = models.ManyToManyField(Subject, related_name='classes')
  level = models.IntegerField(default=0, unique=True)
  current_price = models.IntegerField(default=0)
  new_student_price = models.IntegerField(default=0)

  def __str__(self):
    return self.name


class ClassRoom(TimespamtedModel):
  name = models.CharField(max_length=50)
  classroom_class = models.ForeignKey(
      Class, related_name='classrooms', on_delete=models.CASCADE)


class Professor(User):
  subject = models.ForeignKey(
      Subject, related_name='profs', on_delete=models.CASCADE)
  classes = models.ManyToManyField(Class, related_name="professors")

  def __str__(self):
    return self.name


class Action(TimespamtedModel):
  name = models.CharField(max_length=255)
  user = models.ForeignKey(
      User, related_name='actions', on_delete=models.CASCADE)
