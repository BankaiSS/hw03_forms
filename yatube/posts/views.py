from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from yatube.settings import NUMBER_OF_POSTS

from .forms import PostForm
from .models import Group, Post, User


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, NUMBER_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.all()
    paginator = Paginator(post_list, NUMBER_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'group': group,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    paginator = Paginator(post_list, NUMBER_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'author': author,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'post': post
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author_id = request.user.id
            instance.save()
            user_name = request.user.username
            return redirect("posts:profile", user_name)
    form = PostForm()
    return render(request, "posts/create_post.html", {"form": form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user.id != post.author.id:
        return redirect("posts:post_detail", post.pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("posts:post_detail", post.id)
        return render(request, "posts/create_post.html", {
            "form": form,
            "post": post,
            "is_edit": True,
        })

    form = PostForm(instance=post)
    context = {
        "form": form,
        "is_edit": True,
    }
    return render(request, "posts/create_post.html", context)
