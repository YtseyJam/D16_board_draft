from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from allauth.account.forms import SignupForm
from django.core.mail import send_mail, EmailMultiAlternatives, mail_managers

from board.models import Author


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')

    class Meta:
        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  'password1',
                  'password2',
                  )


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        # registered = Group.objects.get(name="users")
        # user.groups.add(registered)

        subject = 'Добро пожаловать на гильдейскую доску объявлений!'
        text = f'{user.username}, вы успешно зарегистрировались на сайте!'
        html = (
            f'<b>{user.username}</b>, вы успешно зарегистрировались на '
            f'<a href="http://127.0.0.1:8000/board">сайте</a>!'
        )
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[user.email]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()

        mail_managers(
            subject='Новый пользователь!',
            message=f'Пользователь {user.username} успешно зарегистрировался на сайте!'
        )

        return user
