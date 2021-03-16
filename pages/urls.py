from django.urls import path
from .views import home_page_view, login_view

urlpatterns = [
    path('', home_page_view, name='home'),
    path('login/', login_view, name='login'),
]
