from django.urls import path

from .views import class_offer_list, conditions, price_option_list


app_name = 'classes'
urlpatterns = [
    path('', class_offer_list, name='classes'),
    path('ceny/', price_option_list, name='prices'),
    path('regulamin/', conditions, name='conditions'),
]
