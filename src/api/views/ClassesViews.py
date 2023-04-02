from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from ..serializers import ClassLevelSerializer
from ..models import School, User, Role


class ClassLevel(APIView):
  def post(self, request):
    serializer = ClassLevelSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
