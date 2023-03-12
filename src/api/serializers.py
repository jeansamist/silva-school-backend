from rest_framework import serializers
from .models import Professor, School, Class, Subject, User, ClassRoom, Action, Role, Permission


class SchoolSerializer(serializers.ModelSerializer):
  image = serializers.ImageField(required=False)
  classes = serializers.PrimaryKeyRelatedField(
      queryset=Class.objects.all(), many=True)

  users = serializers.PrimaryKeyRelatedField(
      queryset=User.objects.all(), many=True)

  class Meta:
    model = School
    fields = '__all__'


class UserSerailizer(serializers.ModelSerializer):
  # role = serializers.PrimaryKeyRelatedField(
  #     queryset=User.objects.all(), many=False)
  # schools = serializers.PrimaryKeyRelatedField(
  #     queryset=School.objects.all(), many=True)

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
    instance = self.Meta.model(**validated_data)
    if password is not None:
      instance.set_password(password)
    instance.save()
    return instance
