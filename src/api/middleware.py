from django.http.response import JsonResponse
import jwt


class AuthMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    response = self.get_response(request)
    print('\n\n call \n\n')
    return response

  def process_view(self, request, view_func, view_args, view_kwargs):
    print('\n\n process_view \n\n')
    try:
      token = request.headers['Authorization']
      print(jwt.decode(token, 'secret', 'HS256'))

    except:
      # print(request)
      return JsonResponse(data={'detail': 'no token'}, status=400)
