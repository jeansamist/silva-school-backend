import email
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
# from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from ..models import User
import datetime
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

    # if not user.check_password(password):
    #   raise AuthenticationFailed('password is incorrect')

    payload = {
        "id": user.pk,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
        "iat": datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, 'secret', algorithm="HS256")
    return Response({"access_token": token})
