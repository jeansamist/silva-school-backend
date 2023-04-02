from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView
from ..serializers import SchoolSerializer
from ..models import School, User, Role


class SchoolDetailView(APIView):
  def get(selft, request, pk):
    serializer = False
    try:
      user = User.objects.get(pk=request.current_user.pk)
    except:
      return Response({'details': 'You cannot access to a School. Try to login'}, HTTP_401_UNAUTHORIZED)

    if user.role.name == Role.objects.get(name='root').name:
      serializer = SchoolSerializer(School.objects.get(pk=pk))
    elif user.schools.count() > 0:
      if user.schools.filter(pk=pk).count() > 0:
        serializer = SchoolSerializer(user.schools.get(pk=pk))
      else:
        return Response({'details': 'You cannot access to a School'}, HTTP_401_UNAUTHORIZED)
    if serializer == False:
      return Response({'details': 'We cannot provide you a School'}, HTTP_401_UNAUTHORIZED)

    return Response(serializer.data)


class SchoolView(APIView):
  def get(self, request):
    try:

      user = User.objects.get(pk=request.current_user.pk)
      serializer = False

      if user.role.name == Role.objects.get(name='root').name:
        serializer = SchoolSerializer(School.objects.all(), many=True)
      elif user.schools.count() > 0:
        serializer = SchoolSerializer(user.schools, many=True)

      if serializer == False:
        return Response({'details': 'You cannot access to a School'}, HTTP_401_UNAUTHORIZED)

      return Response(serializer.data)
    except:
      return Response({'details': 'You cannot access to a School. Try to login'}, HTTP_401_UNAUTHORIZED)

  def post(self, request):
    serializer = SchoolSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
      action = request.headers['Action-Name']
      if action == 'config':
        if School.objects.all().count() >= 1:
          raise NotAuthenticated({
              'details': "You are not loged as Admin for this action"
          })
    except:
      raise NotAuthenticated({
          'details': "You are not loged as Admin for this action"
      })
    serializer.save()
    return Response(serializer.data)
