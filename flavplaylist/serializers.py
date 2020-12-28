from rest_framework import serializers
from flavplaylist.models import Playlist
from flavaudio.serializers import AudioSerializer


class PlaylistSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    date = serializers.DateTimeField(required=False)
    tracks = AudioSerializer(many=True, read_only=True)

    class Meta:
        model = Playlist
        fields = '__all__'
