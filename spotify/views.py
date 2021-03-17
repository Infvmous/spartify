from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_GET

from .services import (
    spotify_get_authorize_url,
    spotify_handle_authorization_callback,
    spotify_logout
)


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
