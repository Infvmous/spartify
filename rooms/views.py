from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from spotify.decorators import spotify_login_required
from .services import (
    room_update_or_create,
    room_join,
    current_user_host,
    room_get_by_code
)


@require_POST
@spotify_login_required()
def room_create_view(request):
    room = room_update_or_create(request)
    return room_join(request, room.code)


@require_POST
@spotify_login_required()
def room_join_view(request):
    code = request.POST.get('code')
    return room_join(request, code)


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
