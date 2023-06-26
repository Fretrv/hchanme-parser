import os
import re
import random
import time

import requests
from bs4 import BeautifulSoup
from downloader import Downloader


class Parser:

    def __init__(self, startLink):
        self.baseLink = 'https://xxxxx.hentaichan.live'
        self.startLink = startLink

    def get_max_offset(self):
        """

            Пагинация на сайте в виде оступов по 20 постов
            Функция выводит максимальное число отступа

        """
        startPageHtml = self.__get_html(self.startLink)
        offset = startPageHtml.find('div', {'id': 'pagination'})\
            .findAll('a')[-1]\
            .get('href').replace("?offset=", "")
        return (int(offset))

    def __get_request(self, link):
        return requests.get(link)

    def __get_html(self, link):
        response = self.__get_request(link)
        if response.status_code == 200:
            return BeautifulSoup(response.content, 'html.parser')
        else:
            sleeptime = random.randint(15, 45)
            print(f'Error, waiting for {sleeptime}')
            time.sleep(sleeptime)

    def __get_manga_list(self, link):
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
            genres_list = mangaRow.find('div', {'class': 'genre'}).findAll('a')
            genres_list = [genre.text for genre in genres_list]

            # достаем ссылку на мангу
            mangalink = self.baseLink + \
                mangaRow.find('a', {'class': 'title_link'}).get('href')

            # добавляем мангу в список
            manga_list.append({
                'title': title,
                'link': mangalink,
                'genres': genres_list
            })
        return manga_list

    def __get_download_link(self, mangaLink):
        download_page = self.__get_html(
            mangaLink.replace("/manga/", "/download/"))
        return download_page.find('span', {'class': 'attachment'}).a.get('href')

    def parse_page(self, link):
        """

            Метод парсит страницу и скачивает с неё всю мангу 

        """
        manga_list = self.__get_manga_list(link)
        for manga in manga_list:
            print(f"Downloading {manga['title']}")
            dir = os.path.join(os.getcwd(), "manga", manga['title'])
            if os.path.isdir(dir):
                print("Skipping")
                continue
            downloadLink = self.__get_download_link(manga['link'])
            filename = Downloader()
            filename.download(manga['title'], downloadLink)
            time.sleep(5)
