from django.shortcuts import render

from .models import AboutInfo, Teacher


def about(request):
    about_info = AboutInfo.objects.all().first()
    teachers = Teacher.objects.all()
    return render(request, "about/about.html", {'about_info': about_info, 'teachers': teachers})
