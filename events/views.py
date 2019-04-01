from django.shortcuts import render, get_object_or_404
from .models import Event

# Create your views here.
def events(request):
	events = Event.objects.all()
	return render(request, "events/events.html", {'events':events})

def event(request, event_id):
	event = get_object_or_404(Event, id=event_id)
	return render(request,"events/event.html",{'event':event})