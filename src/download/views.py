from django.shortcuts import render
from api.models import Student, ClassRoom
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import io
import random
import string
# Create your views here.


def index(request):
  return render(request, "index.html")


def student_list_pdf(request):

  classroom_id = request.GET.get('classroom_id')

  classroom = ClassRoom.objects.get(pk=classroom_id)
  students = Student.objects.filter(
      classroom=classroom.pk).order_by('first_name')
  boys_nbr = students.filter(sex='M').count()
  girls_nbr = students.filter(sex='F').count()
  context = {'classroom': classroom, 'students': students,
             'nbr_of_student': students.count(), "boys_nbr": boys_nbr, "girls_nbr": girls_nbr}

  template = get_template('student_list_pdf.html')
  html_render = template.render(context)
  result = io.BytesIO()
  pdf = pisa.pisaDocument(io.BytesIO(html_render.encode('UTF-8')), result)

  def random_number(length=8):
    letters = string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
  response = HttpResponse(result.getvalue(), content_type='application/pdf')
  filename = f'{random_number()} - {classroom.class_level.school.name} Students list from {classroom.name}'
  response['Content-Disposition'] = f'attachment; filename="{filename}.pdf"'
  return response
  # return render(request, 'student_list_pdf.html', context)
