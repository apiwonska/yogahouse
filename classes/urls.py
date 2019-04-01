from django.urls import path
from . import views

app_name = 'classes'
urlpatterns = [
    path('', views.classes, name='classes'),
    path('ceny/', views.prices, name='prices'),
    path('regulamin/', views.conditions, name='conditions'),
]
