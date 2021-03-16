from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

from spotify.services import user_authenticated_in_spotify


def spotify_auth_required(view_func) -> HttpResponse:
    """"
    Decorator for views that checks the user is authenticated in Spotify 
    """
    def wrapped_view(request, *args, **kwargs):
        if user_authenticated_in_spotify(request.session.session_key):
            return view_func(request, *args, **kwargs)
        else:
            # TODO: create and render 403 template
            raise PermissionDenied
    return wrapped_view
