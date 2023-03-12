import email
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from django.conf import settings
# from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from ..models import User
import datetime
import time
import jwt


class AuthView(APIView):
  pass


class LoginView(APIView):
  def post(self, request):
    username = request.data['username']
    password = request.data['password']

    user = User.objects.filter(username=username).first()

    if user is None:
      raise AuthenticationFailed('user not found')

    if not user.check_password(password):
      raise AuthenticationFailed('password is incorrect')
    access_payload = {
        "id": user.pk,
        "exp": time.time() + settings.ACCESS_TOKEN_EXPIRES,
    }
    refresh_payload = {
        "id": user.pk,
        "exp": time.time() + settings.REFRESH_TOKEN_EXPIRES,
    }
    print(refresh_payload)
    access_token = jwt.encode(
        access_payload, settings.SECRET_KEY, algorithm="HS256")
    refresh_token = jwt.encode(
        refresh_payload, settings.SECRET_KEY, algorithm="HS256",)
    return Response({"access": access_token, "refresh": refresh_token, "expire": datetime.datetime.now() + datetime.timedelta(seconds=settings.ACCESS_TOKEN_EXPIRES)})
