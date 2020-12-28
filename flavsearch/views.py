import threading
import datetime
import hashlib
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utils.metaparser import AudioMetaParser, MetaNotFoundException
from mutagen.mp3 import MP3
from flavaudio.serializers import AudioSerializer

CACHE = {}


class SearchView(APIView):
    def get(self, request):
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

    # def post(self, request):
    #     index = -1
    #     parser = AudioMetaParser(query_params=query)
    #     cache = CACHE.get(query)
    #     if not cache:
    #         parser.parse_meta_data()
    #         CACHE[query] = parser.temp_storage
    #         cache = CACHE.get(query)
    #
    #     parser.temp_storage = cache
    #
    #     for i in range(len(cache)):
    #         if cache[i]["id"] == pk:
    #             index = i
    #
    #     if index > -1:
    #         now = datetime.datetime.now()
    #         hash_title = hashlib.sha256(str(now).encode("utf-8")).hexdigest()
    #         path = f"media/audio/{hash_title}.mp3"
    #         thread = threading.Thread(target=self.__loader_proc, args=(parser, path, cache, index))
    #         thread.start()
    #         thread.join()

    # @staticmethod
    # def __loader_proc(parser, path, cache, index):
    #     try:
    #         parser.load_data(index, "url", path)
    #
    #         audio_file = MP3(path)
    #         duration = audio_file.info.length
    #         minutes = int(duration // 60)
    #         seconds = int(duration % 60)
    #         if seconds < 10:
    #             seconds = "0" + str(seconds)
    #         repr_duration = str(minutes) + ":" + str(seconds)
    #
    #         img_uri = cache[index]["img"]
    #
    #         if img_uri.split("/")[-1] == "no-cover-150.jpg":
    #             img_uri = "media/covers/default.png"
    #
    #         data = {
    #             "title": cache[index]["title"],
    #             "img_url": img_uri,
    #             "author": cache[index]["artist"],
    #             "src_url": path,
    #             "duration": duration,
    #             "repr_duration": repr_duration
    #         }
    #         audio = AudioSerializer(data=data)
    #         if audio.is_valid():
    #             audio.create(audio.validated_data)
    #     except OSError:
    #         pass
