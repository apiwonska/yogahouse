from django.shortcuts import render, get_object_or_404
from .models import Category, Post

# Create your views here.

def blog(request):
	posts = Post.objects.all()
	categories = Category.objects.all()
	return render(request, "blog/blog.html", {'posts':posts, 'categories': categories})

def blog_post(request, post_id):
	post = get_object_or_404(Post, id=post_id)
	return render(request, "blog/blog_post.html",{'post':post})

def blog_category(request, category_id):
	category = get_object_or_404(Category, id=category_id)
	categories = Category.objects.all()
	return render(request, "blog/blog_category.html",{'category':category, 'categories': categories})