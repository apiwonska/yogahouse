from django.shortcuts import render
from .models import AboutInfo, Teacher

# Create your views here.
def about(request):
	about_info = AboutInfo.objects.all()
	teachers = Teacher.objects.all()
	return render(request, "about/about.html", {'about_info':about_info[0], 'teachers':teachers})