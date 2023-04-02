from django.urls import path
from api.views.userViews import RegisterView
from api.views.schoolViews import SchoolView, SchoolDetailView
from api.views.configViews import ConfigView
from api.views.authView import LoginView, CurrentAuthUserView
from api.views.ClassesViews import ClassLevel
from api.views.tokenViews import RefreshTokenView
urlpatterns = [
    path('user', RegisterView.as_view()),
    path('school', SchoolView.as_view()),
    path('school/<int:pk>', SchoolDetailView.as_view()),
    path('config', ConfigView.as_view()),
    path('auth/login', LoginView.as_view()),
    path('auth/user', CurrentAuthUserView.as_view()),
    path('token/refresh', RefreshTokenView.as_view()),
    path('class', ClassLevel.as_view()),
]
