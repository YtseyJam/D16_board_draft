"""
URL configuration for D16_board_draft project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from board.views import PostDetail, profile, delete_comment, accept_comment, send_newsletter
from board import views as board_views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  # path('accounts/', include('django.contrib.auth.urls')),
                  # path('accounts/', include('accounts.urls')),
                  path('accounts/', include('allauth.urls')),
                  path('accounts/profile/', profile, name='profile'),

                  path('ckeditor/', include('ckeditor_uploader.urls')),
                  path('pages/', include('django.contrib.flatpages.urls')),
                  path('board/', include('board.urls')),

                  path('board/post/<int:pk>/', PostDetail.as_view(), name='post'),
                  path('board/post/add', board_views.add_post, name='add_post'),
                  path('board/post/edit/<int:pk>/', board_views.edit_post, name='edit_post'),
                  path('board/post/<int:pk>/comment/', board_views.add_comment, name='add_comment'),

                  path('comment/delete/<int:pk>/', delete_comment, name='delete_comment'),
                  path('accept_comment/<int:pk>/', accept_comment, name='accept_comment'),
                  path('send-newsletter/', send_newsletter, name='send_newsletter'),



              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
