from django.forms import ModelForm

from .models import Room


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ('guest_can_pause', 'votes_to_skip_song')


class RoomJoinForm(ModelForm):
    class Meta:
        model = Room
        fields = ('code',)
