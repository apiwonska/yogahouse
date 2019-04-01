from django.shortcuts import render
from .models import ClassOffer, Conditions, PriceCategory, PriceDetail, PriceOption

# Create your views here.

def classes(request):
	class_offer = ClassOffer.objects.all()
	return render(request, "classes/classes.html", {"class_offer":class_offer})

def prices(request):	
	prices = PriceOption.objects.all()
	categories = PriceCategory.objects.all()
	return render(request, "classes/prices.html", {'prices':prices, 'categories':categories})

def conditions(request):
	conditions = Conditions.objects.all()
	return render(request, "classes/conditions.html", {'conditions':conditions[0]})