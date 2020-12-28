from rest_framework import serializers
from flavaudio.models import Audio


class AudioSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Audio
        fields = '__all__'
