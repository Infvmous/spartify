from django.db import models


class SpotifyToken(models.Model):
    user = models.CharField(max_length=64, unique=True)
    refresh_token = models.CharField(max_length=160)
    access_token = models.CharField(max_length=160)
    token_type = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_in = models.DateTimeField()

    class Meta:
        db_table = 'spotify_token'

    def __str__(self):
        return self.user