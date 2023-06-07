import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    dict_hw_2 = {}
    api_key: str = os.getenv('YT_API_KEY')

    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """
        Экземпляр инициализируется id канала. Дальше все данные будут добавляться по API.
        """
        self.channel_id = channel_id
        channel = Channel.get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
        # новые атрибуты
        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.url = channel['items'][0]['snippet']['thumbnails']["default"]['url']
        self.subscriberCount = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.viewCount = channel['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f'{self.title}, {self.url}'

    def __add__(self, other):
        return int(self.subscriberCount) + int(other.subscriberCount)

    def __sub__(self, other):
        return int(self.subscriberCount) - int(other.subscriberCount)

    def __gt__(self, other):
        return int(self.subscriberCount) > int(other.subscriberCount)

    def __ge__(self, other):
        return int(self.subscriberCount) >= int(other.subscriberCount)

    def __lt__(self, other):
        return int(self.subscriberCount) < int(other.subscriberCount)

    def __le__(self, other):
        return int(self.subscriberCount) <= int(other.subscriberCount)

    def __eq__(self, other):
        return int(self.subscriberCount) == int(other.subscriberCount)

    def print_info(self) -> None:
        """
        Выводит в консоль информацию о канале.
        """
        print(
            json.dumps(self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute(), indent=2,
                       ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """
        Класс-метод возвращающий объект для работы с YouTube API
        """
        api_key: str = os.getenv('YT_API_KEY')
        object_get = build('youtube', 'v3', developerKey=api_key)
        return object_get

    def to_json(self, file_name):
        """
        Метод сохраняющий в файл значения атрибутов экземпляра `Channel`
        """
        # dict_hw_2 = self.dict_hw_2
        self.dict_hw_2['id'] = self.channel_id
        self.dict_hw_2['title'] = self.title
        self.dict_hw_2['description'] = self.description
        self.dict_hw_2['url'] = self.url
        self.dict_hw_2['subscriberCount'] = self.subscriberCount
        self.dict_hw_2['video_count'] = self.video_count
        self.dict_hw_2['viewCount'] = self.viewCount

        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(self.dict_hw_2, f, indent=2, ensure_ascii=False)
