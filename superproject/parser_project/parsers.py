import re
import httpx
from typing import Optional
from datetime import datetime
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod


class HtmlGetter:

    HEADERS = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.1) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/94.0.4606.61 Safari/537.36",
        "accept": "*/*",
    }

    @staticmethod
    def safe_url(link: str) -> str:
        url = link.strip()
        return url

    def get_html(self, link: str) -> httpx.Response:
        url = self.safe_url(link)
        headers = self.HEADERS
        response = httpx.get(url, headers = headers)
        return response


class UniversalParser(HtmlGetter):

    @staticmethod
    def get_date(text: str) -> str:
        date_regex = [
            r'\d{2} [а-я]* \d{4}',
            r'\d{2}\.\d{2}.\d{4}',
            r'\d{4}\.\d{2}.\d{2}',
        ]
        for item in date_regex:
            date = re.search(item, text)
            if date:
                return date.group(0)

    def parse_html(self, url: str) -> Optional[dict]:
        html = self.get_html(url)
        if html.status_code == 200:
            soup = BeautifulSoup(html, 'lxml')
            title = soup.find('title').get_text()
            body = soup.find('body')
            text_list = []
            count = 0
            for string in body.stripped_strings:
                if count == 100:
                    break
                if len(string) > 7:
                    if 'https' not in string and '@' not in string:
                        if string not in text_list:
                            text_list.append(string.replace('\xa0', ' '))
                            count += 1
            text = ''
            for string in text_list:
                text += f"{string} "
            date = self.get_date(text)
            return {"date": date, "title": title, "link": url, "text": text}
        return html.status_code


class AbstractParserNews(HtmlGetter, ABC):

    @staticmethod
    def get_date_today() -> datetime:
        date = datetime.today()
        return date

    @abstractmethod
    def get_news_list(self) -> list:
        pass

    @abstractmethod
    def get_news_text(self, url: str) -> dict:
        pass


class SputnikParserNews(AbstractParserNews):

    HOST = 'https://sputnik.by'

    def date_format(self) -> str:
        date = self.get_date_today().strftime('/%Y%m%d/')
        return date

    def get_url_news_list(self) -> str:
        url = self.HOST + self.date_format()
        return url

    def get_news_list(self) -> list:
        url = self.get_url_news_list()
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        items = soup.find_all('a', class_='list__title')
        news_list = []
        for item in items:
            news_list.append(
                {
                    "title": item.get("title"),
                    "link": self.HOST + item.get("href")
                }
            )
        return news_list

    def get_news_text(self, url: str) -> dict:
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        body = soup.find_all('div', class_ = 'article__text')
        date = soup.find('div', class_ = 'article__info-date').get_text()
        preview = soup.find('div', class_ = 'article__announce-text').get_text()
        text = preview + ' '
        for item in body:
            text += item.get_text().replace('.', '. ')
        news = {"date": date, "text": text}
        return news


class LentaParserNews(AbstractParserNews):

    HOST = 'https://lenta.ru'

    def date_format(self) -> str:
        date = self.get_date_today().strftime('/%Y/%m/%d/')
        return date

    def get_url_news_list(self) -> str:
        url = self.HOST + '/news' + self.date_format()
        return url

    def get_news_list(self) -> list:
        url = self.get_url_news_list()
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        items = soup.find_all('a', class_ = 'titles')
        news_list = []
        for item in items:
            title = str(item.find('h3', class_ = 'card-title').get_text())
            news_list.append(
                {
                    "title": title.replace('\xa0', ' '),
                    "link": self.HOST + item.get('href')
                }
            )
        return news_list

    def get_news_text(self, url: str) -> dict:
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        body = soup.find('div', class_ = 'b-text clearfix js-topic__text').get_text()
        date = soup.find('div', class_ = 'b-topic__info').get_text()
        preview = soup.find('div', class_ = 'b-topic__title-yandex').get_text()
        text = preview + '. ' + body
        news_text = {"date": date, "text": text}
        return news_text


class EuronewsParserNews(AbstractParserNews):

    HOST = 'https://ru.euronews.com'

    def date_format(self) -> str:
        date = self.get_date_today().strftime('/%Y/%m/%d/')
        return date

    def get_url_news_list(self) -> str:
        url = self.HOST + self.date_format()
        return url

    def get_news_list(self) -> list:
        url = self.get_url_news_list()
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        items = soup.find_all('a', class_ = 'm-object__title__link')
        news_list = []
        for item in items:
            news_list.append(
                {
                    "title": item.get('title'),
                    "link": self.HOST + item.get('href')
                }
            )
        return news_list

    def get_news_text(self, url: str) -> dict:
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        date = str(soup.find('time', class_ = 'c-article-date').get_text()).strip()
        date = date.replace('\xa0', '')
        date = date.replace('•', '')
        date = date.replace('\n           ', '')
        body = soup.find_all('div', class_ = 'c-article-content js-article-content article__content')
        text = ''
        for item in body:
            text = item.get_text().replace('.', '. ')
        news_text = {"date": date, "text": text}
        return news_text
