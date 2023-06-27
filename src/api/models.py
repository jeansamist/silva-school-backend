from django.db import models
import random
from django.contrib.auth.models import Permission
from django.contrib.auth.hashers import (
    check_password,
    make_password,
)
from pathlib import Path
import datetime
import string
# Create your models here.


# def random_filename(ext):
#   letters = string.ascii_letters
#   result_str = ''.join(random.choice(letters) for i in range(100))
#   return result_str + ext


def school_image_upload_path(instance, filename):
  from .functions import random_filename
  ext = Path(filename).suffix
  return 'images/schools/{filename}'.format(filename=random_filename(ext))


def avatar_image_upload_path(instance, filename):
  from .functions import random_filename
  ext = Path(filename).suffix
  return 'images/avatars/{filename}'.format(filename=random_filename(ext))


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
  phone = models.TextField(null=True, blank=True)
  code = models.CharField(unique=True, null=True, blank=True, max_length=10)
  avatar = models.ImageField(
      upload_to=avatar_image_upload_path, blank=True, null=True)
  # avatar = models.ImageField(upload_to=upload_to2, blank=True, null=True)

  def create_code(self):
    letters = string.ascii_uppercase
    numbers = string.digits
    end = ''.join(random.choice(numbers) for i in range(5))
    start = ''.join(random.choice(numbers) for i in range(4))
    middle = ''.join(random.choice(letters) for i in range(1))
    self.code = f'{start}{middle}{end}'

  class Meta:
    abstract = True


class User(Person):
  username = models.CharField(max_length=150, unique=True, help_text=(
      "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."), error_messages={"unique": ("A user with that username already exists."), })
  password = models.TextField()
  role = models.ForeignKey(Role, related_name="users",
                           on_delete=models.CASCADE, blank=True, null=True)
  schools = models.ManyToManyField(
      School, related_name="users", blank=True, null=True)
  _password = None
  REQUIRED_FIELDS = ["username", "password"]

  def is_root(self):
    return self.role.name == Role.objects.get(name='root').name

  def get_full_name(self):
    full_name = "%s %s" % (self.first_name, self.last_name)
    return full_name.strip()

  def set_password(self, raw_password):
    self.password = make_password(raw_password)
    self._password = raw_password

  def check_password(self, raw_password):
    def setter(raw_password):
      self.set_password(raw_password)
      # Password hash upgrades shouldn't be considered password changes.
      self._password = None
      self.save(update_fields=["password"])

    return check_password(raw_password, self.password, setter)


class Subject(TimespamtedModel):
  name = models.CharField(max_length=255)
  coef = models.IntegerField(default=1)
  # classes = models.ManyToManyField(Class, related_name='subjects')


class ClassLevel(TimespamtedModel):
  name = models.CharField(max_length=25)
  school = models.ForeignKey(
      School, related_name='class_levels', on_delete=models.CASCADE)
  subjects = models.ManyToManyField(Subject, related_name='class_levels')
  level = models.IntegerField(default=0, unique=True)
  current_price = models.IntegerField(default=0)
  new_student_price = models.IntegerField(default=0)

  def __str__(self):
    return self.name


class ClassRoom(TimespamtedModel):
  name = models.CharField(max_length=50)
  class_level = models.ForeignKey(
      ClassLevel, related_name='classrooms', on_delete=models.CASCADE)


class Professor(User):
  subject = models.ForeignKey(
      Subject, related_name='professors', on_delete=models.CASCADE)
  class_levels = models.ManyToManyField(ClassLevel, related_name="professors")

  def __str__(self):
    return self.name


class Student(Person):
  register = models.BooleanField(default=False)
  classroom = models.ForeignKey(
      ClassRoom, related_name='students', on_delete=models.CASCADE)


class Action(TimespamtedModel):
  name = models.CharField(max_length=255)
  user = models.ForeignKey(
      User, related_name='actions', on_delete=models.CASCADE)
