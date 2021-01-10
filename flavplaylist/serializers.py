from rest_framework import serializers
from flavplaylist.models import Playlist
from flavaudio.serializers import AudioSerializer
from flavaudio.models import Audio


class PlaylistSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    date = serializers.DateTimeField(required=False)
    tracks = AudioSerializer(many=True, required=False)

    def create(self, validated_data):
        track_list = validated_data.pop("tracks")
        instance = Playlist.objects.create(**validated_data)
        for track in track_list:
            try:
                track_obj = Audio.objects.get(pk=track["id"])
                instance.tracks.add(track_obj)
            except Audio.DoesNotExist:
                pass
        instance.save()
        return None

    def update(self, instance, validated_data):
        instance.tracks.set([])
        track_list = self.validated_data["tracks"]
        for track in track_list:
            try:
                track_obj = Audio.objects.get(pk=track["id"])
                instance.tracks.add(track_obj)
            except Audio.DoesNotExist:
                pass
        instance.title = self.validated_data["title"]
        instance.description = self.validated_data["description"]
        instance.save()
        return instance

    class Meta:
        model = Playlist
        fields = '__all__'
