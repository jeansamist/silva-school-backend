from rest_framework import serializers
from .models import Professor, School, ClassLevel, Subject, User, ClassRoom, Student, Role, Permission


class SchoolSerializer(serializers.ModelSerializer):
  image = serializers.ImageField(required=False)
  class_levels = serializers.PrimaryKeyRelatedField(
      queryset=ClassLevel.objects.all(), many=True)

  users = serializers.PrimaryKeyRelatedField(
      queryset=User.objects.all(), many=True)

  class Meta:
    model = School
    fields = '__all__'


class UserSerailizer(serializers.ModelSerializer):
  # role = serializers.PrimaryKeyRelatedField(
  #     queryset=User.objects.all(), many=False)
  schools = serializers.PrimaryKeyRelatedField(
      queryset=School.objects.all(), many=True)

  class Meta:
    model = User
    fields = '__all__'
    extra_kwargs = {
        'password': {
            'write_only': True
        }
    }

  def create(self, validated_data):

    password = validated_data.pop('password', None)
    schools_data = validated_data.pop('schools', [])
    user = self.Meta.model.objects.create(**validated_data)
    if password is not None:
      user.set_password(password)
    user.schools.set(schools_data)
    user.save()
    return user


class StudentSerializer(serializers.ModelSerializer):
  classroom = serializers.PrimaryKeyRelatedField(
      queryset=ClassRoom.objects.all(), many=False)

  def create(self, validated_data):
    student = self.Meta.model.objects.create(**validated_data)
    student.create_code()
    student.save()
    return student

  class Meta:
    model = Student
    fields = '__all__'


class ClassLevelSerializer(serializers.ModelSerializer):
  school = serializers.PrimaryKeyRelatedField(
      queryset=School.objects.all(), many=False)
  subjects = serializers.PrimaryKeyRelatedField(
      queryset=Subject.objects.all(), many=True)
  classrooms = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

  class Meta:
    model = ClassLevel
    fields = '__all__'


class ClassRoomSerializer(serializers.ModelSerializer):
  students = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
  class_level = serializers.PrimaryKeyRelatedField(
      queryset=ClassLevel.objects.all(), many=False)

  class Meta:
    model = ClassRoom
    fields = '__all__'
