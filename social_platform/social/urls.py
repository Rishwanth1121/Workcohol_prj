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
    path('my-posts/', views.my_posts, name='my_posts'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('search/', views.search_users, name='search_users'),
    path('add-friend/<int:user_id>/', views.add_friend, name='add_friend'),
    path('accept_friend/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject_friend/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
    path('notifications/', views.notifications, name='notifications'),
    path('search/', views.search_page, name='search_page'),     # search UI
    path('search-users/', views.search_users, name='search_users'),
    path('ajax/add_friend/', views.ajax_add_friend, name='ajax_add_friend'),
    path('ajax/cancel_friend/', views.ajax_cancel_friend, name='ajax_cancel_friend'),
    path('send-request/', views.send_friend_request, name='send_friend_request'),
    path('cancel-request/', views.cancel_friend_request, name='cancel_friend_request'),
    path('accept-request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject-request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),

]
