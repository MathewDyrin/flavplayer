from django.db import models


class Audio(models.Model):
    title = models.CharField(max_length=255)
    img_url = models.CharField(max_length=255)
    src_url = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    duration = models.FloatField()
    repr_duration = models.CharField(max_length=10, default="0:00")

    def __str__(self):
        return f"{self.pk} :{self.author} - {self.title}"
