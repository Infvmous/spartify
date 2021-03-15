import requests

from django.shortcuts import redirect
from django.http import JsonResponse

from .services import (
    create_session_if_not_exists, 
    update_or_create_user_tokens,
    get_spotify_authorize_url,
    get_access_and_refresh_tokens
)


def spotify_authorize_view(request):
    if request.method == 'GET':
        return redirect(get_spotify_authorize_url())


def spotify_authorization_callback(request):
    authorization_code = request.GET.get('code')
    authorization_error = request.GET.get('error')

    response = get_access_and_refresh_tokens(authorization_code)

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')

    create_session_if_not_exists(request)
    update_or_create_user_tokens(
        request.session.session_key, refresh_token, access_token, 
        token_type, expires_in)
    return JsonResponse({'status': 'ok', 'msg': 'you have been authorized'})

   