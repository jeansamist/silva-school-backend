import email
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers import UserSerailizer
from ..models import User


class RegisterView(APIView):
  def post(self, request):
    serializer = UserSerailizer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
