from rest_framework import serializers
from .models import Professor, School, ClassLevel, Subject, User, ClassRoom, Action, Role, Permission


class SchoolSerializer(serializers.ModelSerializer):
  image = serializers.ImageField(required=False)
  classes = serializers.PrimaryKeyRelatedField(
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


class ClassLevelSerializer(serializers.ModelSerializer):
  school = serializers.PrimaryKeyRelatedField(
      queryset=School.objects.all(), many=False)
  subjects = serializers.PrimaryKeyRelatedField(
      queryset=Subject.objects.all(), many=True)

  class Meta:
    model = ClassLevel
    fields = '__all__'
