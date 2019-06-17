from django.shortcuts import render, get_object_or_404
from .models import Course, ClassOccurrence, ClassType
from datetime import datetime, date, timedelta
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def class_occurrence_list(request):
    today = datetime.today()
    start_current_week = today - timedelta(days=today.weekday())
    # Parameter 'day' is passed when link to next/previous week is clicked
    day = request.GET.get('day','')
    if day:
        day_date = datetime(int(day[:4]), int(day[5:7]), int(day[8:]))
        start_of_week = day_date - timedelta(days=day_date.weekday())
    else:
        start_of_week = start_current_week
    week_dates = [(start_of_week + timedelta(days=i)).date() for i in range(7)]
    week_dates_str = [date.strftime("%d/%m") for date in week_dates]
    weekdays_names = ['Poniedziałek', 'Wtorek', 'Środa',
                      'Czwartek', 'Piątek', 'Sobota', 'Niedziela']
    # Used to display table and accordeon structure
    weekdays = [(weekdays_names[i], week_dates_str[i], week_dates[i])
                for i in range(7)]
    # Dates in string format used to create links to next and previous week
    # schedule
    start_next_week = (start_of_week + timedelta(days=7)).date().isoformat()
    start_previous_week = (
        start_of_week - timedelta(days=7)).date().isoformat()

    messages = {}
    classtype = request.GET.get('class-type','')
    # Limits shedule display to x weeks starting from current week
    if (start_of_week.date() < start_current_week.date() or
            start_of_week.date() - start_current_week.date() >= timedelta(weeks=3)):
        classes_during_week = []
        messages['week_view'] = 'Grafik niedostępny'
    elif classtype:
        classes_during_week = ClassOccurrence.objects.filter(
            date__in=week_dates,
            cancelled=False,
            course__class_type__slug=classtype
        )
        if classes_during_week.count() == 0:
            messages['week_view'] = 'Brak zaplanowanych zajęć'
    else:
        classes_during_week = ClassOccurrence.objects.filter(
            date__in=week_dates, cancelled=False)
        if classes_during_week.count() == 0:
            messages['week_view'] = 'Brak zaplanowanych zajęć'

    # Needed to create rows in week schedule table for each hour
    start_time = list(set([c.start_time for c in classes_during_week]))
    start_time.sort()
    # Needed to display all types of classes in select form
    class_types = ClassType.objects.all()

    submit = {'modal': '', 'day': '', 'class_id': ''}
    if request.method == "POST":
        user = request.user
        action = request.POST.get('action','')
        class_id = request.POST.get('class-id','')        
        submit['modal'] = request.POST.get('modal','')
        submit['day'] = request.POST.get('day','')
        submit['class_id'] = class_id
        if action == 'sign-up' and user not in class_occurrence.students.all() and class_occurrence.number_of_places_left > 0:
            try:
                class_occurrence = ClassOccurrence.objects.get(pk=int(class_id))
                class_occurrence.students.add(user)
                messages['modal'] = 'Zostałeś zapisany'
            except:
                messages['modal'] = 'Coś poszło nie tak. Spróbuj jeszcze raz.'
        elif action == 'sign-off' and user in class_occurrence.students.all():
            try:
                class_occurrence = ClassOccurrence.objects.get(pk=int(class_id))
                class_occurrence.students.remove(user)
                messages['modal'] = 'Zostałeś wypisany'
            except:
                messages['modal'] = 'Coś poszło nie tak. Spróbuj jeszcze raz.'

    context = {
        'today': today.date(),
        'day': day,
        'weekdays': weekdays,
        'classes_during_week': classes_during_week,
        'class_types': class_types,
        'start_time': start_time,
        'classtype': classtype,
        'start_next_week': start_next_week,
        'start_previous_week': start_previous_week,
        'messages': messages,
        'submit': submit
    }

    return render(request, "schedule/class_occurrence_list.html", context)


@login_required
def user_class_occurrence_list(request):
    messages = {}
    user = request.user
    if request.method == "POST":
        class_id = request.POST.get('class-id','')        
        try:
            class_occurrence = ClassOccurrence.objects.get(id=int(class_id))
            class_occurrence.students.remove(user)
            messages['sign_off'] = "Zostałeś wypisany"
        except:
            messages['sign_off'] = 'Coś poszło nie tak. Spróbuj jeszcze raz.'

    user_classes = ClassOccurrence.objects.filter(students=user).order_by('-date', '-start_time')   
    months = {'styczeń': '1', 'luty': '2', 'marzec': '3', 'kwiecień': '4', 
    		  'maj': '5', 'czerwiec': '6', 'lipiec': '7', 'sierpień': '8', 
    		  'wrzesień': '9', 'październik': '10', 'listopad': '11', 'grudzień': '12'}
    current_year = date.today().year
    # Lists all the years starting with year when user participated in classes
    # for the first time
    if user_classes:
        min_year = user_classes.earliest('date').date.year
        years = [str(y) for y in range(current_year, min_year - 1, -1)]
    else:
        years = []
        messages['class_list'] = "Masz jeszcze żadnych zajęć."

    year = request.GET.get('year','')
    month = request.GET.get('month','')
    if year and not month:
        user_classes = user_classes.filter(date__year=int(year))
    elif month and not year:
        user_classes = user_classes.filter(date__month=int(month))
    elif month and year:
        user_classes = user_classes.filter(
            date__year=int(year), date__month=int(month))
 
    paginator = Paginator(user_classes, 3)
    page = request.GET.get('page')
    user_classes = paginator.get_page(page)

    context = {
        'user_classes': user_classes,
        'months': months,
        'years': years,
        'month': month,
        'year': year,
        'messages': messages
    }
    return render(request, "schedule/user_class_occurrence_list.html", context)
