from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post

# Group Chat View
@login_required
def group_chat_view(request):
    return render(request, 'group_chat.html')

# Home Page View
@login_required
def home_view(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        if content or image:
            Post.objects.create(user=request.user, content=content, image=image)
            return redirect('home')
    
    posts = Post.objects.all().order_by('-created_at')
    members = User.objects.all()
    return render(request, 'home.html', {'posts': posts, 'members': members})

# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# Register View
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        User.objects.create_user(username=username, password=password)
        return redirect('login')
    return render(request, 'register.html')

# All Posts View
@login_required
def all_posts_view(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'all_posts.html', {'posts': posts})

# Members View (Missing one you needed)
@login_required
def members_view(request):
    members = User.objects.all()
    return render(request, 'members.html', {'members': members})
