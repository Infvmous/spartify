from django.shortcuts import render

from spotify.decorators import spotify_login_required
from rooms.forms import RoomForm


@spotify_login_required(reverse_path='login')
def home_page_view(request):
    return render(request, 'home.html', context={'room_form': RoomForm})


def login_view(request):
    return render(request, 'login.html')
