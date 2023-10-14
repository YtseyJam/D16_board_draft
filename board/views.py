from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import PostForm, CommentForm
from .models import Post, Category, Author, Comment

from django.contrib.auth.decorators import login_required


class BoardList(ListView):
    model = Post
    ordering = '-post_datetime'
    template_name = 'board.html'
    context_object_name = 'posts'
    paginate_by = 10


@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post_item = form.save(commit=False)
            post_item.author = request.user.author
            post_item.save()
            return redirect('/board')
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})


@login_required
def edit_post(request, pk=None):
    item = get_object_or_404(Post, id=pk)
    form = PostForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('/board')
    return render(request, 'post_form.html', {'form': form})


@login_required
def add_comment(request, pk=None):
    post = get_object_or_404(Post, id=pk)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('/board')
    else:
        form = CommentForm()

    return render(request, 'add_comment.html', {'form': form})
