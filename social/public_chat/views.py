from django.shortcuts import render
from chatty.models import *

def index(request):
    user_info = AppUser.objects.get(user=request.user)
    return render(request, 'public_chat/public_chat.html', {
        'profile' : user_info
    })

def room(request, room_name):
    user_info = AppUser.objects.get(user=request.user)
    return render(request, 'public_chat/room.html', {
        'profile' : user_info,
        'room_name' : room_name
    })