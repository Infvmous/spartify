from django.http import HttpRequest
from django.shortcuts import redirect
from django.db.models import QuerySet

from .models import Room
from .forms import RoomForm, RoomJoinForm


def room_create_or_get_existing_code(request: HttpRequest) -> Room.code:
    """
    Creating new room if it doesn't exist,
    Return created room code or existing one
    """
    room = room_filter_by_host(request.session.session_key)
    if room.exists():
        return room[0].code
    return room_create(request)


def room_filter_by_host(session_key: Room.host) -> QuerySet:
    return Room.objects.filter(host=session_key)


def room_create(request: HttpRequest) -> Room.code:
    """
    Creating new room using RoomForm,
    Returns created room code
    """
    form = RoomForm(request.POST)
    if form.is_valid():
        room = form.save(commit=False)
        room.host = request.session.session_key
        room.save()
        return room.code


def room_join(request: HttpRequest) -> Room.code:
    """
    Joining room if it does exist, redirect to home if it does not
    """
    code = request.POST.get('code')
    if Room.objects.filter(code=code).exists():
        return redirect('room', code=code)
    # TODO: add popup to show that room doesnt exist
    return redirect('home')


def room_get_by_code(code: Room.code) -> Room:
    """
    Returns Room by code
    """
    return Room.objects.get(code=code)


def current_user_host(session_key: Room.host, room_code: Room.code) -> bool:
    """
    Returns True if user is host in current room
    """
    room_host = room_get_by_code(room_code).host
    return True if session_key == room_host else False
