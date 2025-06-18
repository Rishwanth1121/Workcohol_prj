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
    path('posts/', views.posts_page, name='all_posts'),
    path('posts/<int:post_id>/like/', views.like_post, name='like_post'),
    path('posts/<int:post_id>/comment/', views.comment_post, name='comment_post'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('members/', views.members_view, name='members'),
    path('search/', views.search_view, name='search'),
    path('notifications/', views.notification_page, name='notifications'),
]
