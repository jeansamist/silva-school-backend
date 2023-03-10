import email
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers import UserSerailizer
from ..models import User, Role


class RegisterView(APIView):
  def post(self, request):
    serializer = UserSerailizer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
      action = request.headers['Action-Name']
      if action == 'config':
        if not User.objects.filter(role=Role.objects.get(name='root').pk).count() == 1:
          serializer.validated_data.update(
              role=Role.objects.get(name='root'))
        else:
          return Response({
              'details': "Admin are all ready configured"
          })
    except:
      pass
    serializer.save()
    return Response(serializer.data)
