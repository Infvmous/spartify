from django.urls import path

from .views import (
    spotify_authorize_view,
    spotify_authorization_callback,
    spotify_logout_view,
    spotify_current_song
)


urlpatterns = [
    path('authorize/', spotify_authorize_view, name='spotify_authorize'),
    path('redirect/', spotify_authorization_callback),
    path('logout/', spotify_logout_view, name='spotify_logout'),
    path('current-song/', spotify_current_song),
]
