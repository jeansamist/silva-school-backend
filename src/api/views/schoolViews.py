from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers import SchoolSerializer
from ..models import School, User, Role


class SchoolView(APIView):
  def post(self, request):
    serializer = SchoolSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
      action = request.headers['Action-Name']
      if action == 'config':
        if School.objects.all().count() >= 1:
          return Response({
              'details': "You are not loged as Admin for this action"
          })
    except:
      pass
    serializer.save()
    return Response(serializer.data)