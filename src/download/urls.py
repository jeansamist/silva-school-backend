from django.urls import path
from .views import index, student_list_pdf
urlpatterns = [
    path('', index),
    path('student_list_pdf', student_list_pdf),
]
