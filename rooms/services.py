from django.http import HttpRequest
from django.shortcuts import redirect

from .models import Room
from .forms import RoomForm


def room_get_created_or_existing_code(request: HttpRequest) -> Room.code:
    """
    Returns existing room code or creating new room and return it's code
    """
    room = Room.objects.filter(host=request.session.session_key)
    if room.exists():
        # Return existing room code
        return room[0].code
    # Create if room doesn't exist
    return room_create(request)
        

def room_create(request: HttpRequest) -> Room.code:
    """
    Creating new room using RoomForm,
    Returns created room code
    """
    form = RoomForm(request.POST)
    if form.is_valid():
        new_room = form.save(commit=False)
        new_room.host = request.session.session_key
        new_room.save()
        return new_room.code




