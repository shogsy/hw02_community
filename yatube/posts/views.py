from django.shortcuts import get_object_or_404, render

from .models import Group, Post

POSTS_NUM = 10


def index(request):
    posts = Post.objects.order_by('-pub_date')[:POSTS_NUM]
    template = 'posts/index.html'
    context = {
        'posts': posts,
    }
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:POSTS_NUM]
    context = {
        'group': group,
        'posts': posts,
    }
    template = 'posts/group_list.html'
    return render(request, template, context)
