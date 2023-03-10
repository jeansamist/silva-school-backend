from rest_framework.response import Response
from rest_framework.views import APIView


class ConfigView(APIView):
  def get(self, request):
    return Response({'config': True})
