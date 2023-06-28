from pymongo import MongoClient


class Manga:

    def __init__(self, title: str, link: str, genres: list):
        self.title = title
        self.link = link
        self.genres = genres

    def get_params(self) -> dict:
        return {
            'title': self.title,
            'link': self.link,
            'genres': self.genres
        }


class Client:
    """

        Клиент для работы с базой данных манги

    """

    def __init__(self, mongodb: str) -> None:
        self.client = MongoClient(mongodb)
        self.db = self.client['manga-db']
        if not (self.db.list_collection_names()):
            self.db.create_collection('manga')
        self.collection = self.db['manga']

    def insert_one_manga(self, manga: Manga) -> None:
        self.collection.insert_one(manga.get_params())

    def insert_many_manga(self, mangalist: list) -> None:
        self.collection.insert_many([manga.get_params()
                                    for manga in mangalist])
