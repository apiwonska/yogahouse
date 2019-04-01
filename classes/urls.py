from django.urls import path
from . import views

urlpatterns = [
    path('', views.classes, name='classes'),
    path('ceny/', views.prices, name='prices'),
    path('regulamin/', views.conditions, name='conditions'),
]
