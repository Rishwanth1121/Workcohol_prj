from django.shortcuts import render
from .models import Message

def room(request, room_name):
    username = request.user.username if request.user.is_authenticated else "Anonymous"
    messages = Message.objects.filter(room_name=room_name).order_by('timestamp')
    return render(request, "chat/room.html", {
        "room_name": room_name,
        "username": username,
        "messages": messages,
    })

