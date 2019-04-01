from django.urls import path
from . import views

urlpatterns = [
    path('', views.schedule, name='schedule'),
    path('class_type/<int:class_type_id>/', views.schedule_class_type, name='schedule_class_type'),
]