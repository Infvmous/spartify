from django.shortcuts import redirect

from spotify.services import user_authenticated_in_spotify


def spotify_login_required(viewname='login'):
    """"
    Decorator for views that checks the user is logged in Spotify,
    redirects to login page if not
    """
    def decorator(view_func):
        def wrapped_view(request, *args, **kwargs):
            if user_authenticated_in_spotify(request.session.session_key):
                return view_func(request, *args, **kwargs)
            else:
                return redirect(viewname)
        return wrapped_view
    return decorator
