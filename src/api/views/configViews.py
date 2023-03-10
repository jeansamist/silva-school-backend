from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import User, School
from django.http.response import JsonResponse


class ConfigView(APIView):
  def get(self, request):

    admin_exist = User.objects.filter(role=1).count() == 1
    school_exist = School.objects.all().count() >= 1
    config = {'admin_exist': admin_exist, 'school_exist': school_exist}
    if not admin_exist or not school_exist:
      try:
        action = request.headers['Action-Name']
        if not action == 'config':
          return Response(config)
      except:
        return Response(config)

    return Response(config)
