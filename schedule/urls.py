from django.urls import path
from . import views

app_name = 'schedule'
urlpatterns = [
	path('', views.class_occurrence_list, name='week_view'),
	path('twoje-zajecia/', views.user_class_occurrence_list, name='user_class_list'),
]