from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from .models import Group, Post

POSTS_NUM = 10


def index(request):
    posts = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(posts, POSTS_NUM)
    template = 'posts/index.html'
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.all().filter(group=group).order_by('-pub_date')
    paginator = Paginator(posts, POSTS_NUM)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    template = 'posts/group_list.html'
    return render(request, template, context)
