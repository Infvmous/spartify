from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from spotify.decorators import spotify_login_required
from .services import (
    room_create_or_get_existing_code,
    room_join,
    current_user_host,
    room_get_by_code
)


@require_POST
@spotify_login_required()
def room_create_view(request):
    return redirect('room', code=room_create_or_get_existing_code(request))


@require_POST
@spotify_login_required()
def room_join_view(request):
    return room_join(request)


@spotify_login_required()
def room_view(request, code):
    room = room_get_by_code(code)
    session_key = request.session.session_key
    context = {
        'host': current_user_host(session_key, code),
        'code': code,
        'votes_to_skip_song': room.votes_to_skip_song,
        'guest_can_pause': room.guest_can_pause
    }
    return render(request, 'room.html', context=context)
