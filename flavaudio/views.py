import os
import threading
import datetime
import hashlib
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from mutagen.mp3 import MP3
from utils.metaparser import AudioMetaParser, MetaNotFoundException
from flavaudio.models import Audio
from flavaudio.serializers import AudioSerializer


CACHE = {}


def loader_proc(parser, path, cache, index, serialzer):
    try:
        parser.load_data(index, "url", path)

        audio_file = MP3(path)
        duration = audio_file.info.length
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        if seconds < 10:
            seconds = "0" + str(seconds)
        repr_duration = str(minutes) + ":" + str(seconds)

        img_uri = cache[index]["img"]

        if img_uri.split("/")[-1] == "no-cover-150.jpg":
            img_uri = "media/covers/default.png"

        data = {
            "title": cache[index]["title"],
            "img_url": img_uri,
            "author": cache[index]["artist"],
            "src_url": path,
            "duration": duration,
            "repr_duration": repr_duration
        }

        audio = serialzer(data=data)
        if audio.is_valid():
            audio.create(audio.validated_data)
            return True
        return False

    except OSError:
        pass


class AudioPagination(PageNumberPagination):
    page_size = 100


class AudioViewSet(viewsets.ModelViewSet):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer
    pagination_class = AudioPagination

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('query_params')
        if query:
            if CACHE.get(query):
                data = {
                    "data": CACHE[query]
                }
                return Response(data)
            audio_parser = AudioMetaParser(query_params=query)
            try:
                audio_parser.parse_meta_data()
                CACHE[query] = audio_parser.temp_storage
                data = {
                    "data": CACHE[query]
                }
                return Response(data)
            except MetaNotFoundException:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def add(self, request):
        query_data = {
            "query": request.data["query"],
            "track_id": request.data["track_id"]
        }
        index = -1
        parser = AudioMetaParser(query_params=query_data["query"])
        cache = CACHE.get(query_data["query"])
        if not cache:
            parser.parse_meta_data()
            CACHE[query_data["query"]] = parser.temp_storage
            cache = CACHE.get(query_data["query"])

        parser.temp_storage = cache

        for i in range(len(cache)):
            if cache[i]["id"] == query_data["track_id"]:
                index = i
        if index > -1:
            now = datetime.datetime.now()
            hash_title = hashlib.sha256(str(now).encode("utf-8")).hexdigest()
            path = f"media/audio/{hash_title}.mp3"
            thread = threading.Thread(target=loader_proc, args=(parser, path, cache, index, self.serializer_class))
            thread.start()
            thread.join()
            return Response(status=status.HTTP_201_CREATED)
        return Response({"msg": "ok"})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        audio_path = instance.src_url
        self.perform_destroy(instance)
        try:
            os.remove(audio_path)
        except FileNotFoundError:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)





