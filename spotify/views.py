from django.shortcuts import redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_GET

from .services import (
    spotify_get_authorize_url,
    spotify_handle_authorization_callback,
    spotify_logout,
    spotify_send_request,
)
from rooms.services import room_get_if_exist_by_code


@require_GET
def spotify_authorize_view(request):
    return HttpResponseRedirect(spotify_get_authorize_url())


@require_GET
def spotify_authorization_callback(request):
    spotify_handle_authorization_callback(request)
    return redirect('home')


@require_GET
def spotify_logout_view(request):
    spotify_logout(request.session.session_key)
    return redirect('login')


def spotify_current_song(request):
    room_code = request.session.get('room_code')
    room = room_get_if_exist_by_code(room_code)[0]
    response = spotify_send_request(room.host, 'player/currently-playing')
    return JsonResponse({'song': response.json()})
