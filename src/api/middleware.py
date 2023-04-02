from django.http.response import JsonResponse
import jwt
from .models import User, Permission, Role, School
from django.conf import settings

PERMISSIONS = [
    Permission(name="create", action_name="create"),
    Permission(name="update", action_name="update"),
    Permission(name="delete", action_name="delete"),
]


class AuthMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    response = self.get_response(request)
    return response

  def process_view(self, request, view_func, view_args, view_kwargs):
    db_is_config = Permission.objects.all().count() >= 1

    if not db_is_config:
      for permission in PERMISSIONS:
        permission.save()
      Role.objects.create(name="root", id=1).permissions.set(
          Permission.objects.all())

    admin_exist = User.objects.filter(role=1).count() == 1
    school_exist = School.objects.all().count() >= 1
    config = {'admin_exist': admin_exist, 'school_exist': school_exist}
    if not admin_exist or not school_exist:
      try:
        action = request.headers['Action-Name']
        if not action == 'config':
          return JsonResponse(data=config, status=200)
      except:
        return JsonResponse(data=config, status=200)
    try:
      access = request.headers['Authorization']
      payload = jwt.decode(access, settings.SECRET_KEY, algorithms="HS256")

      user = User.objects.get(pk=payload['id'])
      print(user)
      if user is None:
        error = {'detail': 'User not found'}
        return JsonResponse(data=error, status=403)
      else:
        request.current_user = user
    except:
      pass
