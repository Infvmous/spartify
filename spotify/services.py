import requests
from datetime import timedelta
from typing import NoReturn, Dict

from django.utils import timezone

from .models import SpotifyToken
from config.settings import (
    SPOTIFY_REDIRECT_URI, 
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET, 
    SPOTIFY_SCOPES
)


def create_session_if_not_exists(request) -> NoReturn:
    if not request.session.exists(request.session.session_key):
        request.session.create()


def get_spotify_authorize_url() -> str:
    return requests.Request(
        'GET', 'https://accounts.spotify.com/authorize', params={
            'scope': SPOTIFY_SCOPES,
            'response_type': 'code',
            'redirect_uri': SPOTIFY_REDIRECT_URI,
            'client_id': SPOTIFY_CLIENT_ID
        }).prepare().url


def get_access_and_refresh_tokens(authorization_code: str) -> Dict:
    return requests.post(
        'https://accounts.spotify.com/api/token', data={
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': SPOTIFY_REDIRECT_URI,
            'client_id': SPOTIFY_CLIENT_ID,
            'client_secret': SPOTIFY_CLIENT_SECRET
        }).json()


def update_or_create_user_tokens(
        session_key: str, 
        refresh_token: str,
        access_token: str,
        token_type: str,
        expires_in: int) -> NoReturn:
    tokens = _get_user_tokens(session_key)
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if tokens:
        # Update tokens
        tokens.update(refresh_token=refresh_token, access_token=access_token,
            token_type=token_type, expires_in=expires_in) 
    else:
        # Create tokens for user (session_key)
        SpotifyToken.objects.create(
            user=session_key, refresh_token=refresh_token,
            access_token=access_token, token_type=token_type,
            expires_in=expires_in)
           

def _get_user_tokens(session_key: str) -> Dict:
    user_tokens = SpotifyToken.objects.filter(user=session_key)
    if user_tokens.exists():
        return user_tokens
        