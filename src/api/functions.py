import random
import string
from rest_framework.exceptions import AuthenticationFailed
from .models import User


def random_string(length=8):
  letters = string.ascii_letters
  result_str = ''.join(random.choice(letters) for i in range(length))
  return result_str


def random_filename(ext):
  return random_string(100) + ext


def authentificate(username, password):

  user = User.objects.filter(username=username).first()

  if user is None:
    raise AuthenticationFailed('user not found')

  if not user.check_password(password):
    raise AuthenticationFailed('password is incorrect')

  return {"id": user.pk}
