from rest_framework import viewsets
from flavaudio.models import Audio
from flavaudio.serializers import AudioSerializer


class AudioViewSet(viewsets.ModelViewSet):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer


