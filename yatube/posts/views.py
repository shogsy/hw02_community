from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from .forms import PostForm
from .models import Group, Post, User

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


def profile(request, username):
    author = get_object_or_404(User, username=username)
    user = request.user
    author_post = author.posts.all()
    paginator = Paginator(author_post, POSTS_NUM)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': author,
        'user': user,
        'page_obj': page_obj,
    }
    template = 'posts/profile.html'
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    group = post.group
    author = post.author
    posts_count = author.posts.count()
    context = {
        'post': post,
        'group': group,
        'posts_count': posts_count,
    }
    template = 'posts/post_detail.html'
    return render(request, template, context)


# Страница для создания новых постов. Доступна только авторизованным
@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if request.GET or not form.is_valid():
        template = 'posts/create_post.html'
        return render(request, template, {'form': form})

    post = form.save(commit=False)
    post.author = request.user
    form.save()
    return redirect('posts:index')


# Страница для редактирования постов. Доступна только авторизованным
@login_required
def post_edit(request, post_id):
    # Проверка на владельца поста. Если != пользователь, выдать 403
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return HttpResponseForbidden('Не достаточно прав на редактирование')
    form = PostForm(request.POST, instance=post)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.save()
        return redirect(reverse('posts:post_detail', kwargs={
            'post_id': post_id}))
    form = PostForm(instance=post)
    template = 'posts/create_post.html'
    context = {'form': form,
               'post': post,
               'is_edit': True}
    return render(request, template, context)
