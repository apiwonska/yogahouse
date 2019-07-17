from django.urls import path

from .views import post_detail, post_list, search

app_name = 'blog'
urlpatterns = [
    path('', post_list, name='posts'),
    path('search/', search, name='search'),
    path('post/<int:post_id>/', post_detail, name='post'),
]
