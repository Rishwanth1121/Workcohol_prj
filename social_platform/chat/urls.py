from django.urls import path
from django.shortcuts import render
from . import views

urlpatterns = [
    path('<str:room_name>/', views.room, name='room'),
    path('group_chat/', lambda request: render(request, 'chat/group_chat.html'), name='group_chat'),
]
