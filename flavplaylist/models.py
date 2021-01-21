from django.db import models
from django.utils import timezone
from flavaudio.models import Audio


class Playlist(models.Model):
    title = models.CharField(max_length=25)
    img_url = models.CharField(max_length=255)
    description = models.CharField(max_length=60)
    date = models.DateTimeField(default=timezone.now)
    tracks = models.ManyToManyField(Audio)

    def __str__(self):
        return f"{self.pk} : {self.title}"

    class Meta:
        ordering = ['-pk']