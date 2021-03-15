from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import reverse

from spotify.services import user_authenticated_in_spotify


def rooms_home_page_view(request):
    if user_authenticated_in_spotify(request.session.session_key):
        return JsonResponse({'status': 'ok', 'mgs': 'authenticated'})
    return HttpResponseRedirect(reverse('home'))

