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
    """Create user session"""
    if not request.session.exists(request.session.session_key):
        request.session.create()


def get_spotify_authorize_url() -> str:
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


def get_access_and_refresh_tokens(authorization_code: str) -> Dict:
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
        *,
        session_key: str, 
        refresh_token: str,
        access_token: str,
        token_type: str,
        expires_in: int) -> NoReturn:
    """Update or create user Spotify tokens"""
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
           

def user_authenticated_in_spotify(session_key: str) -> bool:
    """Returns True if user spotify tokens exists and False if not, also
    updates it"""
    tokens = _get_user_tokens(session_key)
    if tokens:
        expiry = tokens[0].expires_in
        if expiry <= timezone.now():
            _refresh_user_tokens(session_key)
        return True
    return False


def spotify_logout(session_key: str) -> NoReturn:
    """Deletes user spotify tokens"""
    tokens = _get_user_tokens(session_key)
    tokens.delete()


def _get_user_tokens(session_key: str) -> Dict:
    """Returns user tokens if exists"""
    user_tokens = SpotifyToken.objects.filter(user=session_key)
    if user_tokens.exists():
        return user_tokens


def _refresh_user_tokens(session_key: str) -> NoReturn:
    """Refreshes user tokens"""
    refresh_token = _get_user_tokens(session_key)[0].refresh_token
    response = requests.post(
        'https://accounts.spotify.com/api/token', data={
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': SPOTIFY_CLIENT_ID,
            'client_secret': SPOTIFY_CLIENT_SECRET
        }).json()
    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')
    update_or_create_user_tokens(
        session_key=session_key, 
        refresh_token=refresh_token, 
        access_token=response.get('access_token'), 
        token_type=response.get('token_type'), 
        expires_in=response.get('expires_in'))

        