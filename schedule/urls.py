from django.urls import path

from .views import class_occurrence_list, user_class_occurrence_list

app_name = 'schedule'
urlpatterns = [
    path('', class_occurrence_list, name='week_view'),
    path('twoje-zajecia/', user_class_occurrence_list, name='user_class_list'),
]
