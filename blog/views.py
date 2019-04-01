from django.shortcuts import render, get_object_or_404
from .models import Category, Post

# Create your views here.

def post_list(request):
	posts = Post.objects.all()
	categories = Category.objects.all()
	return render(request, "blog/post_list.html", {'posts':posts, 'categories': categories})

def post_detail(request, post_id):
	post = get_object_or_404(Post, id=post_id)
	return render(request, "blog/post_detail.html",{'post':post})

def category_detail(request, category_id):
	category = get_object_or_404(Category, id=category_id)
	categories = Category.objects.all()
	return render(request, "blog/category_detail.html",{'category':category, 'categories': categories})