from django.urls import path
from api.views.userViews import RegisterView
from api.views.schoolViews import SchoolView
from api.views.configViews import ConfigView
from api.views.authView import LoginView
from api.views.tokenViews import RefreshTokenView
urlpatterns = [
    path('user', RegisterView.as_view()),
    path('school', SchoolView.as_view()),
    path('config', ConfigView.as_view()),
    path('auth/login', LoginView.as_view()),
    path('token/refresh', RefreshTokenView.as_view()),
]
