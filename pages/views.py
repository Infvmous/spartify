from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect

from spotify.services import user_authenticated_in_spotify


def home_page_view(request):
    if user_authenticated_in_spotify(request.session.session_key):
        return HttpResponseRedirect(reverse('rooms_home'))
    return render(request, 'home.html')
