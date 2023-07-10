from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
)
from rest_framework.views import APIView
from django.core.paginator import Paginator
from ..serializers import StudentSerializer
from ..models import Student, User


class StudentDetailView(APIView):
    def get_student(self, pk):
        try:
            return Student.objects.get(pk=pk)
        except:
            return {"error": "Student {id} does not found :(".format(id=pk)}

    def put(self, request, student_pk):
        student = self.get_student(student_pk)

        try:
            user = User.objects.get(pk=request.current_user.pk)
        except:
            return Response(
                {"details": "You cannot access to a Student Service. Try to login"},
                HTTP_401_UNAUTHORIZED,
            )

        try:
            if user.is_root():
                serializer = StudentSerializer(student, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
            else:
                return Response({"details": "Try to login"}, HTTP_401_UNAUTHORIZED)
        except:
            return Response(
                {"details": "You cannot access to a Student Service. Try to login"},
                HTTP_401_UNAUTHORIZED,
            )

    def delete(self, request, student_pk):
        student = self.get_student(student_pk)

        try:
            user = User.objects.get(pk=request.current_user.pk)
        except:
            return Response(
                {"details": "You cannot access to a Student Service. Try to login"},
                HTTP_401_UNAUTHORIZED,
            )

        try:
            if user.is_root():
                student.delete()
                return Response(
                    {"details": "Student has been deleted"}, HTTP_204_NO_CONTENT
                )
            else:
                return Response({"details": "Try to login"}, HTTP_401_UNAUTHORIZED)
        except:
            return Response(
                {"details": "You cannot access to a Student Service. Try to login"},
                HTTP_401_UNAUTHORIZED,
            )

    def get(self, request, student_pk):
        try:
            user = User.objects.get(pk=request.current_user.pk)
        except:
            return Response(
                {"details": "You cannot access to a Student Service. Try to login"},
                HTTP_401_UNAUTHORIZED,
            )

        student = self.get_student(student_pk)
        try:
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        except:
            return Response(student, status=HTTP_404_NOT_FOUND)


class StudenListView(APIView):
    def get(self, request, class_level_pk, classroom_pk):
        serializer = False
        try:
            user = User.objects.get(pk=request.current_user.pk)
        except:
            return Response(
                {"details": "You cannot access to a Student Service. Try to login"},
                HTTP_401_UNAUTHORIZED,
            )

        try:
            page = int(request.GET.get("page"))
        except:
            page = False

        try:
            nbr = int(request.GET.get("nbr_of_elements"))
        except:
            nbr = 5

        if page:
            queryset = Student.objects.filter(classroom=classroom_pk).order_by("-id")
            paginator = Paginator(queryset, nbr)

            if page > paginator.num_pages:
                page = paginator.num_pages

            students = paginator.page(page)
        else:
            students = Student.objects.filter(classroom=classroom_pk).order_by("-id")
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)


class StudentView(APIView):
    def post(self, request):
        serializer = False
        try:
            user = User.objects.get(pk=request.current_user.pk)
        except:
            return Response(
                {"details": "You cannot access to a Student Service. Try to login"},
                HTTP_401_UNAUTHORIZED,
            )

        if user.is_root():
            serializer = StudentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({"details": "Try to login"}, HTTP_401_UNAUTHORIZED)
