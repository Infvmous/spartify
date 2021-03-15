from django.urls import path

from .views import spotify_authorize_view, spotify_authorization_callback


urlpatterns = [
    path('authorize/', spotify_authorize_view, name='spotify_authorize'),
    path('redirect/', spotify_authorization_callback),
]
