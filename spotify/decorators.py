from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import reverse

from spotify.services import user_authenticated_in_spotify


def spotify_login_required(reverse_path: str='home') -> HttpResponse:
    """"
    Decorator for views that checks the user is logged in Spotify,
    redirects if not
    """
    def decorator(view_func):
        def wrapped_view(request, *args, **kwargs):
            if user_authenticated_in_spotify(request.session.session_key):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse(reverse_path))
        return wrapped_view
    return decorator
