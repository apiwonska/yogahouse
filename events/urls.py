from django.urls import path

from .views import event_detail, event_list

app_name = 'events'
urlpatterns = [
    path('', event_list, name='events'),
    path('<int:event_id>/', event_detail, name='event'),
]
