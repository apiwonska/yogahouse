from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog, name='blog'),
    path('post/<int:post_id>', views.blog_post, name='blog_post'),
    path('category/<int:category_id>', views.blog_category, name='blog_category'),
]
