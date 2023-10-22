from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

from ckeditor.fields import RichTextField


class Author(models.Model):
    """
    every registered user could be an author and post to the board
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    TANK = 'TANK'
    HEALER = 'HEAL'
    DAMAGE_DEALER = 'DDDD'
    TRADER = 'TRDE'
    GUILD_MASTER = 'GMGM'
    QUESTER = 'QUST'
    BLACKSMITH = 'BLCK'
    TAYLOR = 'TLOR'
    POTIONMAKER = 'POTM'
    WIZARD = 'WIZZ'
    CATEGORY_CHOICES = [
        (TANK, 'Танки'),
        (HEALER, 'Хилы'),
        (DAMAGE_DEALER, 'ДД'),
        (TRADER, 'Торговцы'),
        (GUILD_MASTER, 'Гилдмастеры'),
        (QUESTER, 'Квестгиверы'),
        (BLACKSMITH, 'Кузнецы'),
        (TAYLOR, 'Кожевники'),
        (POTIONMAKER, 'Зельевары'),
        (WIZARD, 'Мастера заклинаний'),
    ]
    name = models.CharField(max_length=4, choices=CATEGORY_CHOICES, unique=True)

    def __str__(self):
        return dict(self.CATEGORY_CHOICES)[self.name]


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_datetime = models.DateTimeField(auto_now_add=True)
    post_title = models.CharField(max_length=200)
    post_body = RichTextUploadingField(config_name='default', external_plugin_resources=[(
        'youtube',
        '/static/var/ckeditor/ckeditor/plugins/youtube/',
        'plugin.js',
    )],
                                       )

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    slug = models.SlugField(default='', blank=True)
    comments = models.ManyToManyField(User, through='Comment', related_name='comments')

    def __str__(self):
        return f'{self.post_title.title()}: {self.post_body[:100]}... | {self.category}'

    def get_absolute_url(self):
        return reverse('post', args=[str(self.id)])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.post_title)
        super().save(*args, **kwargs)


class Comment(models.Model):
    text = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)


# новостная рассылка
class Newsletter(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
