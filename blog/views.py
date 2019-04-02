from django.shortcuts import render, get_object_or_404
from .models import Category, Post
from django.db.models import Q
from django.core.paginator import Paginator


def post_list(request):
	post_list = Post.objects.all()
	paginator = Paginator(post_list, 3)
	page = request.GET.get('page')
	posts = paginator.get_page(page)

	categories = Category.objects.all()	

	return render(request, "blog/post_list.html", {'posts':posts, 'categories': categories})

def post_detail(request, post_id):
	post = get_object_or_404(Post, id=post_id)
	return render(request, "blog/post_detail.html",{'post':post})

def category_detail(request, category_id):
	category = get_object_or_404(Category, id=category_id)
	categories = Category.objects.all()
	return render(request, "blog/category_detail.html",{'category':category, 'categories': categories})

def search(request):
	query = request.GET.get('q')
	if query:
	 results = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
	else:
		 results = Post.objects.all()
	paginator = Paginator(results, 3)
	page = request.GET.get('page')
	posts = paginator.get_page(page)

	categories = Category.objects.all()	

	return render(request, "blog/post_list.html", {'posts':posts, 'categories': categories, 'query':query})