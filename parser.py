import os
import sys
import argparse
import re
import random
import time

import requests
from bs4 import BeautifulSoup
from downloader import Downloader
from db.manga_db import Manga, Client


def create_args_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--mongodb', default='mongodb://192.168.1.31:27017/')
    return parser


class Parser:

    def __init__(self, startLink: str) -> None:
        self.baseLink = 'https://xxxxx.hentaichan.live'
        self.startLink = startLink
        args_parser = create_args_parser()
        namespace = args_parser.parse_args(sys.argv[1:])
        self.mongodbclient = Client(namespace.mongodb)

    def get_max_offset(self) -> int:
        """

            Пагинация на сайте в виде оступов по 20 постов
            Функция выводит максимальное число отступа

        """
        startPageHtml = self.__get_html(self.startLink)
        offset = startPageHtml.find('div', {'id': 'pagination'})\
            .findAll('a')[-1]\
            .get('href').replace("?offset=", "")
        return (int(offset))

    def __get_request(self, link: str) -> requests.models.Request:
        return requests.get(link)

    def __get_html(self, link: str) -> BeautifulSoup:
        response = self.__get_request(link)
        if response.status_code == 200:
            return BeautifulSoup(response.content, 'lxml')
        else:
            sleeptime = random.randint(15, 45)
            print(f'Error, waiting for {sleeptime}')
            time.sleep(sleeptime)
            self.__get_html(link)

    def __get_manga_list(self, link: str) -> list:
        """

            Функция возвращает список из объектов с Названием, Ссылкой, и тэгами Манги на странице

        """
        manga_list = []

        # ищем все теги с мангой
        mangaRows = self.__get_html(link).findAll(
            "div", {"class": "content_row"})

        for mangaRow in mangaRows:

            # формируем названием манги, очищая её от запретных символов
            pattern = '[^a-zA-Zа-яА-Я!0-9\-()\ ]'
            title = re.sub(pattern, "", mangaRow.get('title'))

            # формируем список жанров
            genres = mangaRow.find('div', {'class': 'genre'}).findAll('a')
            genres = [genre.text for genre in genres]

            # достаем ссылку на мангу
            mangalink = self.baseLink + \
                mangaRow.find('a', {'class': 'title_link'}).get('href')

            # добавляем мангу в список
            manga = Manga(title, mangalink, genres)
            manga_list.append(manga)
        return manga_list

    def __get_download_link(self, mangaLink: str) -> str:
        download_page = self.__get_html(
            mangaLink.replace("/manga/", "/download/"))
        return download_page.find('span', {'class': 'attachment'}).a.get('href')

    def parse_page(self, link: str) -> None:
        """

            Метод парсит страницу и скачивает с неё всю мангу 

        """
        manga_list = self.__get_manga_list(link)
        for manga in manga_list:
            print(f"Downloading {manga.title}")
            dir = os.path.join(os.getcwd(), "manga", manga.title)
            if os.path.isdir(dir):
                print("Skipping")
                continue
            downloadLink = self.__get_download_link(manga.link)
            filename = Downloader()
            filename.download(manga.title, downloadLink)
            self.mongodbclient.insert_one_manga(manga)
            time.sleep(5)
