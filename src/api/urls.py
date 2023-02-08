from django.urls import path
from api.views.userViews import RegisterView
from api.views.authView import LoginView
urlpatterns = [
    path('user', RegisterView.as_view()),
    path('auth/login', LoginView.as_view()),
]
