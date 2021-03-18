from django.http import HttpRequest
from django.shortcuts import redirect, get_object_or_404
from django.db.models import QuerySet

from .models import Room
from .forms import RoomForm, RoomJoinForm


def room_create_or_update(request: HttpRequest) -> Room.code:
    """
    Creating new room if it doesn't exist,
    Return created room code or existing one
    """
    room = room_get_if_exist(request.session.session_key)
    return room_update(request, room[0]) if room else room_create(request)


def room_get_if_exist(session_key: Room.host) -> QuerySet[Room]:
    """
    Returns QuerySet object with Room object inside if exist
    """
    room = Room.objects.filter(host=session_key)
    if room.exists():
        return room


def room_update(request: HttpRequest, room: Room) -> Room.code:
    """
    Updating room guest_can_pause and votes_to_skip_song fields
    Return room code
    """
    form = RoomForm(request.POST)
    if form.is_valid():
        room.guest_can_pause = form.cleaned_data.get('guest_can_pause')
        room.votes_to_skip_song = form.cleaned_data.get(
            'votes_to_skip_song')
        room.save(update_fields=['guest_can_pause', 'votes_to_skip_song'])
        return room.code


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
