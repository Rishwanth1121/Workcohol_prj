from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Count, Q
from .models import Notification
from .models import Post, Like, Comment, UserProfile
from django.shortcuts import get_object_or_404, redirect
from .models import FriendRequest
from django.http import JsonResponse
import json

from django.http import JsonResponse
import json

@login_required
def ajax_add_friend(request):
    if request.method == "POST":
        data = json.loads(request.body)
        to_user_id = data.get("user_id")
        to_user = get_object_or_404(User, id=to_user_id)

        # Check for existing request
        friend_request, created = FriendRequest.objects.get_or_create(
            from_user=request.user, to_user=to_user
        )

        if created:
            # Send a notification to the receiving user
            Notification.objects.create(
                user=to_user,
                message=f"{request.user.username} sent you a friend request."
            )

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def ajax_cancel_friend(request):
    if request.method == "POST":
        data = json.loads(request.body)
        to_user_id = data.get('user_id')
        to_user = get_object_or_404(User, id=to_user_id)

        FriendRequest.objects.filter(from_user=request.user, to_user=to_user).delete()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})

# Example inside post creation view
def create_post(request):
    if request.method == 'POST':
        content = request.POST['content']
        image = request.FILES.get('image')

        post = Post.objects.create(user=request.user, content=content, image=image)

        Notification.objects.create(
            user=request.user,
            message=f"You posted: {content[:30]}..."
        )

        return redirect('home')

@login_required
def notification_page(request):
    notifications = request.user.notifications.all().order_by('-created_at')
    friend_requests = FriendRequest.objects.filter(to_user=request.user)
    return render(request, 'notifications.html', {
        'notifications': notifications,
        'friend_requests': friend_requests
    })

@login_required
def profile_view(request):
    profile = request.user.userprofile
    friends = profile.friends.all()
    return render(request, 'profile.html', {'profile': profile, 'friends': friends})


@login_required
def update_profile(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        profile.role = request.POST.get('role')
        profile.facebook = request.POST.get('facebook')
        profile.twitter = request.POST.get('twitter')
        profile.instagram = request.POST.get('instagram')
        profile.linkedin = request.POST.get('linkedin')

        if request.FILES.get('profile_image'):
            profile.profile_image = request.FILES['profile_image']

        profile.save()
        return redirect('profile')

    return render(request, 'edit_profile.html', {'profile': profile})


@login_required
def home_view(request):
    user = request.user
    unread_count = user.notifications.filter(is_read=False).count() if hasattr(user, 'notifications') else 0
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        if content or image:
            Post.objects.create(user=request.user, content=content, image=image)
            Notification.objects.create(
                user=request.user,
                message=f"{request.user.username} posted: {content[:30]}..."
            )
            return redirect('home')

    posts = Post.objects.all().order_by('-created_at')
    trending = ["#AI", "#StartupLife", "#Photography", "#RemoteWork"]

    context = {
        'posts': posts,
        'trending': trending,
        'unread_notification_count': unread_count,
    }

    return render(request, 'home.html', context)


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    existing_like = Like.objects.filter(user=user, post=post).first()
    if existing_like:
        existing_like.delete()
    else:
        Like.objects.create(user=user, post=post)

    return redirect(request.META.get('HTTP_REFERER', 'posts'))


@login_required
def comment_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        Comment.objects.create(post=post, user=request.user, text=request.POST.get('comment'))
    return redirect(request.META.get('HTTP_REFERER', 'posts'))


@login_required
def posts_page(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        if content or image:
            Post.objects.create(user=request.user, content=content, image=image)
        return redirect('all_posts')

    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'posts.html', {'posts': posts})


@login_required
def group_chat_view(request):
    return render(request, 'group_chat.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            UserProfile.objects.get_or_create(user=user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email:
            messages.error(request, "Email is required.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register')

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            UserProfile.objects.create(user=user)
            return redirect('login')
        except IntegrityError:
            messages.error(request, "User could not be created.")
            return redirect('register')

    return render(request, 'register.html')


@login_required
def all_posts_view(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'all_posts.html', {'posts': posts})


@login_required
def members_view(request):
    profiles = UserProfile.objects.select_related('user').all()
    return render(request, 'members.html', {'profiles': profiles})


@login_required
def search_view(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(username__icontains=query).exclude(id=request.user.id) if query else []
    sent_requests = FriendRequest.objects.filter(from_user=request.user).values_list('to_user_id', flat=True)

    return render(request, 'search_results.html', {
        'query': query,
        'users': users,
        'sent_requests': sent_requests,
    })

@login_required
def mark_notifications_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return redirect('home')

@login_required
def my_posts(request):
    posts = Post.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_posts.html', {'posts': posts})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        post.delete()
    return redirect(request.META.get('HTTP_REFERER', 'posts'))

@login_required
def search_page(request):
    return render(request, 'search_page.html')

def search_users(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(username__icontains=query).exclude(id=request.user.id) if query else []
    sent_requests = FriendRequest.objects.filter(from_user=request.user).values_list('to_user_id', flat=True)
    return render(request, 'search_results.html', {
        'users': users,
        'query': query,
        'sent_requests': list(sent_requests)
    })


@login_required
def add_friend(request, user_id):
    if request.method == "POST":
        from_user = request.user
        to_user = get_object_or_404(User, id=user_id)

        if from_user != to_user:
            friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)

            # ✅ Add this to create a notification entry
            if created:
                Notification.objects.create(
                    user=to_user,
                    message=f"{from_user.username} sent you a friend request."
                )

    return JsonResponse({'status': 'sent'})


@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    from_user = friend_request.from_user

    # Add each other to friends list (You must define this logic or use a ManyToMany)
    request.user.profile.friends.add(from_user.profile)
    from_user.profile.friends.add(request.user.profile)

    friend_request.delete()
    return redirect('notifications')

@login_required
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    friend_request.delete()
    return redirect('notifications')

@login_required
def send_friend_request(request):
    if request.method == "POST":
        to_user_id = request.POST.get('to_user_id')
        to_user = get_object_or_404(User, id=to_user_id)
        friend_request, created = FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
        if created:
            return JsonResponse({'status': 'sent'})
        return JsonResponse({'status': 'exists'})
    return JsonResponse({'status': 'invalid'}, status=400)

@login_required
def cancel_friend_request(request):
    if request.method == "POST":
        to_user_id = request.POST.get('to_user_id')
        to_user = get_object_or_404(User, id=to_user_id)
        FriendRequest.objects.filter(from_user=request.user, to_user=to_user).delete()
        return JsonResponse({'status': 'cancelled'})
    return JsonResponse({'status': 'invalid'}, status=400)

@login_required
def notifications(request):
    friend_requests = FriendRequest.objects.filter(to_user=request.user)
    activity_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications.html', {
        'friend_requests': friend_requests,
        'notifications': activity_notifications
    })


from django.contrib import messages

@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    from_user = friend_request.from_user

    # Add each other as friends
    request.user.userprofile.friends.add(from_user.userprofile)
    from_user.userprofile.friends.add(request.user.userprofile)

    friend_request.delete()
    messages.success(request, f"You are now friends with {from_user.username}")
    return redirect('notifications')


@login_required
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    from_user = friend_request.from_user
    friend_request.delete()
    messages.warning(request, f"Friend request from {from_user.username} declined")
    return redirect('notifications')
