from django.http import HttpResponse


def rooms_home_page_view(request):
    return HttpResponse('dashboard')
