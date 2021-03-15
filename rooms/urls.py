from django.urls import path
from .views import rooms_home_page_view


urlpatterns = [
    path('', rooms_home_page_view, name='rooms_home'),
]
