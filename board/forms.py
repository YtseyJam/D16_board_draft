from django.forms import ModelForm
from .models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = [
            'post_title',
            'post_body',
            'category',

        ]
        labels = {
            'post_title': 'Заголовок',
            'post_body': 'Текст',
            'category': 'Категория'
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
