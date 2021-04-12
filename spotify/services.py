import requests
from requests import Response
from datetime import timedelta

from django.utils import timezone
from django.http import HttpRequest

from .models import SpotifyToken
from rooms.models import Room
from config.settings import (
    SPOTIFY_REDIRECT_URI,
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    SPOTIFY_SCOPES,
    SPOTIFY_API_URL = 'https://api.spotify.com/v1/me/'
)


def spotify_send_request(
        session_key: Room.host,
        endpoint: str,
        method: str = 'GET') -> Response:
    """
    Sending http request to Spotify Web API
    """
    tokens = _get_user_tokens(session_key)[0]
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + tokens.access_token
    }
    url = SPOTIFY_API_URL + endpoint
    response = requests.request(method, url, headers=headers)
    return response


def create_session_if_not_exists(request: HttpRequest) -> None:
    """Create user session"""
    if not request.session.exists(request.session.session_key):
        request.session.create()


def spotify_get_authorize_url() -> str:
    """Returns spotify authorize url"""
    return requests.get(
        'https://accounts.spotify.com/authorize',
        params={
            'scope': SPOTIFY_SCOPES,
            'response_type': 'code',
            'redirect_uri': SPOTIFY_REDIRECT_URI,
            'client_id': SPOTIFY_CLIENT_ID,
            'show_dialog': True
        }).url


def get_access_and_refresh_tokens(authorization_code: str) -> SpotifyToken:
    """Returns access and refresh tokens from Spotify by using
    authorization code"""
    return requests.post(
        'https://accounts.spotify.com/api/token', data={
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': SPOTIFY_REDIRECT_URI,
            'client_id': SPOTIFY_CLIENT_ID,
            'client_secret': SPOTIFY_CLIENT_SECRET
        }).json()


def update_or_create_user_tokens(
        session_key: Room.host,
        refresh_token: SpotifyToken.refresh_token,
        access_token: SpotifyToken.access_token,
        token_type: SpotifyToken.token_type,
        expires_in_seconds: int) -> None:
    """Update or create user Spotify tokens"""
    tokens = _get_user_tokens(session_key)
    expires_in = timezone.now() + timedelta(seconds=expires_in_seconds)
    if tokens:
        tokens.update(refresh_token=refresh_token, access_token=access_token,
                      token_type=token_type, expires_in=expires_in)
    else:
        SpotifyToken.objects.create(
            user=session_key, refresh_token=refresh_token,
            access_token=access_token, token_type=token_type,
            expires_in=expires_in)


def user_authenticated_in_spotify(session_key: Room.host) -> bool:
    """Returns True if user has spotify tokens and update them if
    it's expired, False if user is not authenticated"""
    tokens = _get_user_tokens(session_key)
    if tokens:
        expiry = tokens[0].expires_in
        if expiry <= timezone.now():
            _spotify_refresh_user_tokens(session_key)
        return True
    return False


def spotify_logout(session_key: Room.host) -> None:
    """Deletes user spotify tokens"""
    _get_user_tokens(session_key).delete()


def _get_user_tokens(session_key: Room.host) -> SpotifyToken:
    """Returns user tokens if exists"""
    user_tokens = SpotifyToken.objects.filter(user=session_key)
    if user_tokens.exists():
        return user_tokens


def _spotify_refresh_user_tokens(session_key: Room.host) -> None:
    """Refreshes user tokens"""
    refresh_token = _get_user_tokens(session_key)[0].refresh_token
    response = requests.post(
        'https://accounts.spotify.com/api/token', data={
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': SPOTIFY_CLIENT_ID,
            'client_secret': SPOTIFY_CLIENT_SECRET
        }).json()
    update_or_create_user_tokens(
        session_key, refresh_token, response.get('access_token'),
        response.get('token_type'), response.get('expires_in'))


def spotify_handle_authorization_callback(request: HttpRequest) -> None:
    """
    Getting access and refresh tokens by Spotify auth code received
    after user authorization, creating new user session if it does
    not exist and updating or creating user tokens
    """
    authorization_code = request.GET.get('code')
    # TODO: handle authorization error
    authorization_error = request.GET.get('error')
    response = get_access_and_refresh_tokens(authorization_code)
    create_session_if_not_exists(request)
    update_or_create_user_tokens(
        request.session.session_key, response.get('refresh_token'),
        response.get('access_token'), response.get('token_type'),
        response.get('expires_in'))
