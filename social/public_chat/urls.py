from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('chat/', login_required(login_url='../login/')(views.index), name='index'),
    path('chat/<str:room_name>/', login_required(login_url='../login/')(views.room), name='room'),
]