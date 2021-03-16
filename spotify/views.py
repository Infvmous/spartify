from django.shortcuts import redirect, reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_GET

from .services import (
    create_session_if_not_exists, 
    update_or_create_user_tokens,
    get_spotify_authorize_url,
    get_access_and_refresh_tokens,
    spotify_logout
)


@require_GET
def spotify_authorize_view(request):
    return redirect(get_spotify_authorize_url())


@require_GET
def spotify_authorization_callback(request):
    authorization_code = request.GET.get('code')
    # TODO: handle authorization error
    authorization_error = request.GET.get('error')

    response = get_access_and_refresh_tokens(authorization_code)

    create_session_if_not_exists(request)
    update_or_create_user_tokens(
        session_key=request.session.session_key, 
        refresh_token=response.get('refresh_token'),
        access_token=response.get('access_token'),
        token_type=response.get('token_type'),
        expires_in=response.get('expires_in'))
    return HttpResponseRedirect(reverse('home'))


@require_GET
def spotify_logout_view(request):
    spotify_logout(request.session.session_key)
    return HttpResponseRedirect(reverse('login'))


   