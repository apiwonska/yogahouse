from django.shortcuts import render, get_object_or_404
from .models import Course, ClassOccurrence, ClassType
from datetime import datetime, date, timedelta



def class_occurrence_list(request):
	today = datetime.today()
	start_current_week = today - timedelta(days = today.weekday())	
	# Parameter 'day' is passed when link to next/previous week is clicked
	day = request.GET.get('day')
	if day:	
		day_date = datetime(int(day[:4]),int(day[5:7]),int(day[8:]))
		start_of_week = day_date - timedelta(days = day_date.weekday())
	else:		
		start_of_week = start_current_week
	week_dates = [(start_of_week + timedelta(days=i)).date() for i in range(7)]
	week_dates_str = [date.strftime("%d/%m") for date in week_dates]
	weekdays_names = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota', 'Niedziela']
	# Used to display table and accordeon structure
	weekdays = [(weekdays_names[i], week_dates_str[i], week_dates[i]) for i in range(7)]
	# Dates in string format used to create links to next and previous week schedule 
	start_next_week = (start_of_week + timedelta(days=7)).date().isoformat()
	start_previous_week = (start_of_week - timedelta(days=7)).date().isoformat()
	
	message = ''
	classtype = request.GET.get('class-type')	
	# Limits shedule display to x weeks starting from current week
	if (start_of_week.date() < start_current_week.date() or 
		start_of_week.date() - start_current_week.date() >= timedelta(weeks=3)) :
		classes_during_week = []
		message = 'Grafik niedostępny'
	elif classtype:
		classes_during_week = ClassOccurrence.objects.filter(
			date__in=week_dates, 
			cancelled=False,
			course__class_type__slug=classtype
			)
		if classes_during_week.count() == 0:
			message = 'Brak zaplanowanych zajęć'
	else:
		classes_during_week = ClassOccurrence.objects.filter(date__in=week_dates, cancelled=False)
		if classes_during_week.count() == 0:
			message = 'Brak zaplanowanych zajęć'

	# Needed to create rows in week schedule table for each hour
	start_time = list(set([c.start_time for c in classes_during_week]))
	start_time.sort()
	# Needed to display all types of classes in select form
	class_types = ClassType.objects.all()	
	
	return render(request, "schedule/class_occurrence_list.html", {
		'today':today.date(),
		'day': day,
		'weekdays':weekdays,
		'classes_during_week':classes_during_week, 
		'class_types':class_types, 
		'start_time':start_time,
		'classtype':classtype,
		'start_next_week':start_next_week,
		'start_previous_week':start_previous_week,
		'message': message
		})

