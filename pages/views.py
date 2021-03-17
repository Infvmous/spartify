from django.shortcuts import render

from spotify.decorators import spotify_login_required
from rooms.forms import RoomCreateForm, RoomJoinForm


@spotify_login_required()
def home_page_view(request):
    context = {
        'room_create_form': RoomCreateForm(),
        'room_join_form': RoomJoinForm(initial={'code': None})
    }
    return render(request, 'home.html', context=context)


def login_view(request):
    return render(request, 'login.html')
