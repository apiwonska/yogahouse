from django.shortcuts import render, get_object_or_404
from .models import ClassInSchedule, ClassType, StartTime

# Create your views here.

def schedule(request):
	class_in_schedule = ClassInSchedule.objects.all()
	class_types = ClassType.objects.all()
	start_time = StartTime.objects.all()
	days_of_week = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota', 'Niedziela']
	return render(request, "schedule/schedule.html", {
		'class_in_schedule':class_in_schedule, 'class_types':class_types, 'start_time':start_time, 'days_of_week':days_of_week})


def schedule_class_type(request, class_type_id):
	class_type = get_object_or_404(ClassType, id=class_type_id)
	class_types = ClassType.objects.all()
	start_time = StartTime.objects.all()
	days_of_week = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota', 'Niedziela']
	return render(request, "schedule/schedule_class_type.html", {
		'class_type': class_type, 'class_types':class_types, 'start_time':start_time, 'days_of_week':days_of_week})