from django.forms import ModelForm

from .models import Room


class RoomCreateForm(ModelForm):
    class Meta:
        model = Room
        fields = ['guest_can_pause', 'votes_to_skip_song']


    