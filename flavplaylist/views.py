from rest_framework import viewsets
from flavplaylist.serializers import PlaylistSerializer
from flavplaylist.models import Playlist


class PlayListViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

