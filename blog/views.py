from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Category, Post


def post_list(request):
    post_list = Post.objects.all()
    published_posts = [post for post in post_list if post.was_published()]

    paginator = Paginator(published_posts, 3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    categories = Category.objects.all()

    return render(request, "blog/post_list.html", {'posts': posts, 'categories': categories})


def search(request):
    query = request.GET.get('q')
    category = request.GET.get('cat')
    order = request.GET.get('order')

    if category and query:
        results = Post.objects.filter(category__slug=category).filter(
            Q(title__icontains=query) | Q(content__icontains=query))
    elif category:
        results = Post.objects.filter(category__slug=category)
    elif query:
        results = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query))
    else:
        results = Post.objects.all()

    if order:
        if order == 'n':
            results = results.order_by('-created')
        elif order == 'o':
            results = results.order_by('created')

    paginator = Paginator(results, 3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    categories = Category.objects.all()
    return render(
        request,
        "blog/post_list.html",
        {'posts': posts, 'categories': categories,
            'query': query, 'category': category, 'order': order}
    )


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "blog/post_detail.html", {'post': post})
