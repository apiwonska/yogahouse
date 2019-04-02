from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.post_list, name='posts'),
    path('results', views.search, name='search'),
    path('post/<int:post_id>', views.post_detail, name='post'),
    path('category/<int:category_id>', views.category_detail, name='category'),
]
