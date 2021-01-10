import os
import base64
import datetime
import hashlib
from io import BytesIO
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from PIL import Image
from flavplaylist.serializers import PlaylistSerializer
from flavplaylist.models import Playlist


class PlayListViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    def create(self, request, *args, **kwargs):
        img_data_r = request.data["img_base64data"]
        webp_hb64 = "data:image/webp;base64,"
        jpeg_hb64 = "data:image/jpeg;base64,"
        img_data = None
        if webp_hb64 in img_data_r:
            img_data = img_data_r.split(webp_hb64)[1]
        if jpeg_hb64 in img_data_r:
            img_data = img_data_r.split(jpeg_hb64)[1]
        img = base64.b64decode(img_data)
        now = datetime.datetime.now()
        hash_title = hashlib.sha256(str(now).encode("utf-8")).hexdigest()
        path = f"media/covers/{hash_title}.jpeg"

        stream = BytesIO(img)
        file = Image.open(stream)
        height = file.height
        width = file.width

        if height == width:
            file.save(path)

        if height < width:
            cropped = file.crop((0, 0, height, height))
            cropped.save(path)

        if height > width:
            cropped = file.crop((0, 0, width, width))
            cropped.save(path)

        request.data.pop("img_base64data")
        data = request.data
        data["img_url"] = path

        playlist = self.serializer_class(data=data)
        if playlist.is_valid():
            playlist.create(playlist.validated_data)
            return Response(playlist.data, status=status.HTTP_201_CREATED)
        return Response(status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        img_path = instance.img_url
        self.perform_destroy(instance)
        try:
            os.remove(img_path)
        except FileNotFoundError:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        img_path = instance.img_url
        data = request.data
        data["img_url"] = img_path
        playlist = self.serializer_class(instance=instance, data=data)
        if playlist.is_valid():
            playlist.update(instance, playlist.validated_data)
        return Response(status=status.HTTP_201_CREATED)
