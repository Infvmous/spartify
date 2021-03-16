from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from spotify.decorators import spotify_login_required
from .services import room_get_created_or_existing_code
from .forms import RoomForm
from .models import Room


@require_POST
@spotify_login_required()
def room_create_view(request):
    return redirect('room', code=room_get_created_or_existing_code(request))

 
@require_POST
@spotify_login_required()
def room_join_view(request):
    # If room exists join
    code = request.POST.get('code')
    if Room.objects.filter(code=code).exists():
        return redirect('room', code=code)
    else:
        return redirect('home')


@spotify_login_required()
def room_view(request, code):
    return JsonResponse({'room': code})
