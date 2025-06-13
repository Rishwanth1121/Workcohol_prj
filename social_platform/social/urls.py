from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('all-posts/', views.all_posts_view, name='all_posts'),
    path('members/', views.members_view, name='members'),
    path('group-chat/', views.group_chat_view, name='group_chat'), 
    path('', views.home_view, name='home'),  # HOME PAGE = /
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('all-posts/', views.all_posts_view, name='all_posts'),
]
