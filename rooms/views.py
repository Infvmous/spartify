from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import reverse, render

from spotify.services import user_authenticated_in_spotify
from .forms import RoomCreateForm


def rooms_home_page_view(request):
    if user_authenticated_in_spotify(request.session.session_key):
        return render(request, 'rooms_home.html', 
            context={'room_create_form': RoomCreateForm(request.POST or None)})
    return HttpResponseRedirect(reverse('home'))


def room_create_view(request):
    if user_authenticated_in_spotify(request.session.session_key):
        return render(request, 'room_create.html')
    return HttpResponseRedirect(reverse('home'))



def room_join_view(request):
    return JsonResponse({'join': 'ok'})

