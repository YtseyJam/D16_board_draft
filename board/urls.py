from django.urls import path
# Импортируем созданное нами представление
from .views import BoardList

urlpatterns = [
    path('', BoardList.as_view(), name='board_list'),

]