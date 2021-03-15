from django.urls import path
from .views import rooms_home_page_view, room_create_view, room_join_view


urlpatterns = [
    path('', rooms_home_page_view, name='rooms_home'),
    path('create/', room_create_view, name='room_create'),
    path('join/', room_join_view, name='room_join'),
]
