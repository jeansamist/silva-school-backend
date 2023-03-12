from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from ..serializers import UserSerailizer
from ..models import User
from django.conf import settings
import datetime
import time
import jwt


class RefreshTokenView(APIView):
  def post(self, request):
    try:
      refresh = request.data['refresh']
      try:
        payload = jwt.decode(refresh, settings.SECRET_KEY, algorithms="HS256")

        user = User.objects.get(pk=payload['id'])

        if user is None:
          raise AuthenticationFailed('user not found')

        access_payload = {
            "id": user.pk,
            "exp": time.time() + settings.ACCESS_TOKEN_EXPIRES,
        }
        refresh_payload = {
            "id": user.pk,
            "exp": time.time() + settings.REFRESH_TOKEN_EXPIRES,
        }
        access_token = jwt.encode(
            access_payload, settings.SECRET_KEY, algorithm="HS256")
        refresh_token = jwt.encode(
            refresh_payload, settings.SECRET_KEY, algorithm="HS256")
        return Response({"access": access_token, "refresh": refresh_token, "expire": datetime.datetime.now() + datetime.timedelta(seconds=settings.ACCESS_TOKEN_EXPIRES)})
      except:
        raise AuthenticationFailed({'details': 'token expired'})
    except:
      raise ValidationError({'details': 'We had a error'})
