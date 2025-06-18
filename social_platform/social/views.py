from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Count, Q
from .models import Notification
from .models import Post, Like, Comment, UserProfile


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
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return render(request, 'notifications.html', {'notifications': notifications})


@login_required
def profile_view(request):
    profile = request.user.userprofile
    return render(request, 'profile.html', {'profile': profile})


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

    return redirect('all_posts')


@login_required
def comment_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        Comment.objects.create(post=post, user=request.user, text=request.POST.get('comment'))
    return redirect('all_posts')


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
    query = request.GET.get('q')
    results = []

    if query:
        results = Post.objects.filter(Q(content__icontains=query) | Q(user__username__icontains=query))

    return render(request, 'search_results.html', {'query': query, 'results': results})


@login_required
def mark_notifications_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return redirect('home')
