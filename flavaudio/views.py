from rest_framework.viewsets import generics
from flavaudio.models import Audio
from flavaudio.serializers import AudioSerializer


class AudioView(generics.ListCreateAPIView):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer
