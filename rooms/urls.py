from django.urls import path
from .views import (
    room_create_view,
    room_join_view,
    room_view,
)


urlpatterns = [
    path('<str:code>', room_view, name='room'),
    path('create/', room_create_view, name='room_create'),
    path('join/', room_join_view, name='room_join'),
]
