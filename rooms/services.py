from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.db.models import QuerySet

from .models import Room
from .forms import RoomForm, RoomJoinForm


def room_update_or_create(request: HttpRequest) -> Room:
    """
    Creating new room if it doesn't exist,
    Return created room code or existing one
    """
    room = room_get_if_exist_by_session_key(request.session.session_key)
    return room_update(request, room) if room else room_create(request)


def room_get_if_exist_by_session_key(session_key: Room.host) -> QuerySet[Room]:
    """
    Returns QuerySet object with Room object inside if exist
    by session_key
    """
    room = Room.objects.filter(host=session_key)
    if room.exists():
        return room


def room_get_if_exist_by_code(code: Room.code) -> QuerySet[Room]:
    """
    Returns QuerySet object with Room object inside if exist by code
    """
    room = Room.objects.filter(code=code)
    if room.exists():
        return room


def room_update(request: HttpRequest, room: QuerySet) -> Room:
    """
    Updating room guest_can_pause and votes_to_skip_song fields
    Return room code
    """
    form = RoomForm(request.POST)
    if form.is_valid():
        room.update(
            guest_can_pause=form.cleaned_data.get('guest_can_pause'),
            votes_to_skip_song=form.cleaned_data.get('votes_to_skip_song'))
        return room[0]


def room_create(request: HttpRequest) -> Room:
    """
    Creating new room using RoomForm,
    Returns created room code
    """
    form = RoomForm(request.POST)
    if form.is_valid():
        room = form.save(commit=False)
        room.host = request.session.session_key
        room.save()
        return room


def room_join(request: HttpRequest, code: Room.code) -> HttpResponse:
    """
    Joining room if it does exist, redirect to home if it does not
    """
    if Room.objects.filter(code=code).exists():
        request.session['room_code'] = code  # Add room_code to room session
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
