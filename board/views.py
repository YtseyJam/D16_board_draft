from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import PostForm, CommentForm
from .models import Post, Category, Author, Comment, Newsletter

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


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
            author, created = Author.objects.get_or_create(
                user=request.user)  # при создании поста залогиненый юзер становится автором
            post_item.author = author
            post_item.save()
            return redirect('/board')
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})


@login_required
def edit_post(request, pk=None):
    item = get_object_or_404(Post, id=pk)

    if item.author != request.user.author:
        return HttpResponseForbidden(render(request, '403.html'))

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

            # отпралвяем оповещение об отклике автору
            author_email = post.author.user.email
            context = {
                'author': post.author.user,
                'post_title': post.post_title,
                'text': comment.text,
            }
            html_message = render_to_string('comment_notification.html', context)
            plain_message = strip_tags(html_message)
            send_mail(
                subject='Новый отклик!',
                message=plain_message,
                from_email='a-re-a@yandex.ru',
                recipient_list=[author_email],
                html_message=html_message,
            )
            return redirect('/board')
    else:
        form = CommentForm()

    return render(request, 'add_comment.html', {'form': form})


@login_required
def delete_comment(request, pk=None):
    comment = get_object_or_404(Comment, id=pk)
    post_author = comment.post.author.user
    if post_author == request.user or comment.user == request.user:
        comment.delete()
    return redirect('profile')


def accept_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)

    if request.method == 'POST':
        comment.accepted = True
        comment.save()

        # отправляем оповещение о принятии отклика
        author_email = comment.user.email
        subject = 'Ваш отклик принят!'
        message = 'Отклик к объявлению "{}" был принят автором.'.format(comment.post.post_title)
        send_mail(subject, message, 'a-re-a@yandex.ru', [author_email])

        return redirect('profile')

    return redirect('profile')


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


@login_required
def profile(request):
    user = request.user
    posts = Post.objects.filter(author=request.user.author).filter(comment__isnull=False).distinct()
    return render(request, 'profile.html', {'user': user, 'posts': posts})


@staff_member_required
def send_newsletter(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        content = request.POST['content']
        newsletter = Newsletter.objects.create(subject=subject, content=content)

        users = User.objects.all()

        for user in users:
            send_mail(subject, content, 'a-re-a@yandex.ru', [user.email])

        return redirect('/board')

    return render(request, 'send_newsletter.html')
