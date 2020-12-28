import requests
from abc import ABC
from bs4 import BeautifulSoup


class MetaNotFoundException(Exception):
    def __str__(self):
        return "meta not found"


class BaseMetaParser(ABC):

    BASE_URI = "https://ruv.hotmo.org"
    SEARCH_ENDPOINT = BASE_URI + "/search?q="

    def __init__(self, query_params):

        self._query_params = "+".join(query_params.lower().split(" "))
        self._query_url = self.SEARCH_ENDPOINT + self._query_params
        self._soup = None
        self._raw_meta = None
        self._temp_meta_storage = []

    def parse_meta_data(self):
        response = requests.get(f"{self._query_url}")
        self._soup = BeautifulSoup(response.content.decode("utf-8"), "html.parser")
        meta_list = self._soup.find("ul", class_="tracks__list")

        if meta_list is None:
            raise MetaNotFoundException

        self._raw_meta = meta_list.find_all("li", class_="tracks__item track mustoggler")

        for item in self._raw_meta:
            meta = item.attrs["data-musmeta"]
            title = item.find("div", class_="track__title").text
            title = title.replace('\n', '').strip()
            artist = item.find("div", class_="track__desc").text
            self._temp_meta_storage.append(self.prepare_meta_set(meta, title, artist))

    def load_data(self, index: int, key: str, path: str):
        url = self.clean_url(self._temp_meta_storage[index][key]) if key == "url" else \
            self.BASE_URI + self.clean_url(self._temp_meta_storage[index][key])
        req = requests.get(url)
        with open(f"{path}", "wb") as f:
            f.write(req.content)

    def prepare_meta_set(self, dirty_set, title, artist):
        dirty_set = dirty_set.split('"')

        clean_set = []
        for i in range(0, len(dirty_set)):
            if dirty_set[i] not in ('"', '{', '}', ':', ','):
                clean_set.append(dirty_set[i])

        single_audio_meta = dict()
        for j in range(0, len(clean_set) - 1, 2):
            meta_key = clean_set[j]
            meta_value = clean_set[j + 1]
            if meta_key == "url":
                meta_value = self.clean_url(meta_value)
            if meta_key == "img":
                meta_value = self.BASE_URI + self.clean_url(meta_value)
            if meta_key == "artist":
                meta_value = artist
            if meta_key == "title":
                meta_value = title
            single_audio_meta[meta_key] = meta_value

        return single_audio_meta

    @staticmethod
    def clean_url(dirty_url):
        return "".join([i for i in dirty_url if i != "\\"])

    @property
    def temp_storage(self):
        return self._temp_meta_storage

    @temp_storage.setter
    def temp_storage(self, value):
        self._temp_meta_storage = value


class AudioMetaParser(BaseMetaParser):

    def __init__(self, query_params):
        super().__init__(query_params)

    @property
    def audio_urls(self):
        return [self.clean_url(item["url"]) for item in self._temp_meta_storage]

    @property
    def img_urls(self):
        return [self.BASE_URI + self.clean_url(item["img"]) for item in self._temp_meta_storage]


class ImgMetaParser(BaseMetaParser):
    def __init__(self, query_params):
        super().__init__(query_params)

    @property
    def img_urls(self):
        return [self.clean_url(item["img"]) for item in self._temp_meta_storage]


if __name__ == '__main__':
    query = input("Enter artist name or track title:")
    parser = AudioMetaParser(query_params=query)
    parser.parse_meta_data()
    parser.load_data(0, "url", "mp3", "audio")

    # img_parser = ImgMetaParser(query_params=query)
    # img_parser.parse_meta_data()
    # img_parser.load_data(0, "img", "jpg", "covers")
