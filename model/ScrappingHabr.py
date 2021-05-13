import requests
import re
from bs4 import BeautifulSoup


class ScrappingHabr():

    def __init__(self, *args):
        if isinstance(args[0], list):
            self.KEYWORDS = args[0]
        else:
            self.KEYWORDS = args
        self._SEARCH_PATTERNS = '|'.join(self.KEYWORDS)
        self.url = 'https://habr.com/ru/all/'

    @staticmethod
    def requests_soup(url):
        response = requests.get(url)
        if not response:
            raise ValueError("response is not valid")

        soup = BeautifulSoup(response.text, features="html.parser")
        return soup

    def get_post_preview(self):
        """Поиск по всей доступной preview-информации"""
        soup_preview = ScrappingHabr.requests_soup(self.url)
        for article in soup_preview.find_all('article', class_='post'):
            data = article.find('span', class_='post__time').text
            title = article.find('a', class_='post__title_link').text
            href = article.find('a', class_='post__title_link').attrs.get('href')
            if re.search(self._SEARCH_PATTERNS, article.text):
                print(f'Дата: {data}\nЗаголовок: {title}\nСсылка: {href}\n')

    def get_post_full(self):
        """Поиск по всей доступной preview-информации и если не нашлось по post_full(детальной страницы)"""
        soup_preview = ScrappingHabr.requests_soup(self.url)
        for article in soup_preview.find_all('article', class_='post'):
            data = article.find('span', class_='post__time').text
            title = article.find('a', class_='post__title_link').text
            href = article.find('a', class_='post__title_link').attrs.get('href')
            soup_post_full = ScrappingHabr.requests_soup(href)
            if re.search(self._SEARCH_PATTERNS, article.text) or \
                    re.search(self._SEARCH_PATTERNS, soup_post_full.find('div', class_='post__wrapper').text):
                print(f'Дата: {data}\nЗаголовок: {title}\nСсылка: {href}\n')
