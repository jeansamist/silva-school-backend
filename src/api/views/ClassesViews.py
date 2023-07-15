from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
)
from rest_framework.views import APIView
from ..serializers import ClassLevelSerializer, ClassRoomSerializer
from ..models import ClassLevel, User, Role, ClassRoom


class ClassLevelDetailView(APIView):
    def get(self, request, pk):
        serializer = False
        try:
            user = User.objects.get(pk=request.current_user.pk)
        except:
            return Response(
                {"details": "You cannot access to a School. Try to login"},
                HTTP_401_UNAUTHORIZED,
            )

        if user.role.name == Role.objects.get(name="root").name:
            serializer = ClassLevelSerializer(ClassLevel.objects.get(pk=pk))
        elif user.schools.count() > 0:
            serializer = ClassLevelSerializer(ClassLevel.objects.get(pk=pk))

        if serializer == False:
            return Response(
                {"details": "We cannot provide you a School"}, HTTP_401_UNAUTHORIZED
            )

        return Response(serializer.data)


class ClassRoomView(APIView):
    def get(self, request, class_level_pk):
        classrooms = ClassRoom.objects.filter(class_level=class_level_pk)
        serializer = ClassRoomSerializer(classrooms, many=True)
        return Response(serializer.data)

    def post(self, request, class_level_pk):
        serializer = False
        # try:
        # except:
        #   return Response({'details': 'Error. Try to login'}, HTTP_401_UNAUTHORIZED)

        class_level = ClassLevel.objects.get(pk=class_level_pk)

        try:
            name = "{classname} {name}".format(
                classname=class_level.name, name=request.data["name"]
            )
        except:
            name = "{classname}E{class_id}".format(
                classname=class_level.name,
                class_id=ClassRoom.objects.filter(class_level=class_level_pk).count()
                + 1,
            )
        try:
            user = User.objects.get(pk=request.current_user.pk)
        except:
            return Response(
                {"details": "You cannot access to a ClassLevel. Try to login"},
                HTTP_401_UNAUTHORIZED,
            )

        if user.is_root():
            serializer = ClassRoomSerializer(
                data={"class_level": class_level.pk, "name": name}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({"details": "Try to login"}, HTTP_401_UNAUTHORIZED)


class ClassLevelView(APIView):
    def get(self, request):
        serializer = False

        try:
            user = User.objects.get(pk=request.current_user.pk)
        except:
            return Response(
                {"details": "You cannot access to a ClassLevel. Try to login"},
                HTTP_401_UNAUTHORIZED,
            )

        try:
            school_id = request.headers["School-Id"]
        except:
            return Response(
                {"details": "You cannot access to a ClassLevel. give a School id"},
                HTTP_401_UNAUTHORIZED,
            )

        if user.role.name == Role.objects.get(name="root").name:
            class_levels = ClassLevel.objects.filter(school=school_id)
            serializer = ClassLevelSerializer(class_levels, many=True)
            return Response(serializer.data)
        else:
            if user.schools.filter(pk=school_id).count() == 1:
                class_levels = ClassLevel.objects.filter(school=school_id)
                serializer = ClassLevelSerializer(class_levels, many=True)
                return Response(serializer.data)
            else:
                return Response(
                    {"details": "You cannot access to this School id"},
                    HTTP_401_UNAUTHORIZED,
                )

    def post(self, request):
        serializer = ClassLevelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
