from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.post_list, name='posts'),
    path('search/', views.search, name='search'),
    path('post/<int:post_id>', views.post_detail, name='post'),
]
