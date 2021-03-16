from django.http import JsonResponse
from django.shortcuts import render

from .forms import RoomCreateForm
from spotify.decorators import spotify_auth_required


@spotify_auth_required
def rooms_home_page_view(request):
    return render(request, 'rooms_home.html', 
        context={'room_create_form': RoomCreateForm(request.POST or None)})


@spotify_auth_required
def room_create_view(request):
    return JsonResponse({'create': 'ok'})


@spotify_auth_required
def room_join_view(request):
    return JsonResponse({'join': 'ok'})

