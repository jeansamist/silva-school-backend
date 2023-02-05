class AuthMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    response = self.get_response(request)
    print('\n\n call \n\n')
    return response

  def process_view(self):
    print('\n\n process_view \n\n')
    return None
