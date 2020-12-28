from rest_framework.viewsets import generics
from flavplaylist.serializers import PlaylistSerializer
from flavplaylist.models import Playlist


class PlayListView(generics.ListCreateAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

