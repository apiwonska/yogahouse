from django.urls import path

from .views import post_detail, post_list

app_name = 'blog'
urlpatterns = [
    path('', post_list, name='posts'),
    path('post/<int:post_id>/', post_detail, name='post'),
]
