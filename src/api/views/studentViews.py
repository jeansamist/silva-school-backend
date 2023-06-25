from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from django.core.paginator import Paginator
from ..serializers import StudentSerializer
from ..models import Student, User


class StudenListView(APIView):
  def get(self, request, class_level_pk, classroom_pk):
    serializer = False
    try:
      user = User.objects.get(pk=request.current_user.pk)
    except:
      return Response({'details': 'You cannot access to a Student Service. Try to login'}, HTTP_401_UNAUTHORIZED)

    try:
      page = int(request.GET.get('page'))
    except:
      page = False

    try:
      nbr = int(request.GET.get('nbr_of_elements'))
    except:
      nbr = 5

    if page:
      queryset = Student.objects.filter(classroom=classroom_pk).order_by('-id')
      paginator = Paginator(queryset, nbr)

      if page > paginator.num_pages:
        page = paginator.num_pages

      students = paginator.page(page)
    else:
      students = Student.objects.filter(classroom=classroom_pk).order_by('-id')
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)


class StudentView(APIView):

  def post(self, request):
    serializer = False
    try:
      user = User.objects.get(pk=request.current_user.pk)
    except:
      return Response({'details': 'You cannot access to a Student Service. Try to login'}, HTTP_401_UNAUTHORIZED)

    if user.is_root():
      serializer = StudentSerializer(data=request.data)
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
      else:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    else:
      return Response({'details': 'Try to login'}, HTTP_401_UNAUTHORIZED)
