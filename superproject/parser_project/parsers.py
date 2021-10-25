import re
import pytz
import httpx
import logging
from typing import Optional, Union, List
from datetime import datetime
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.INFO)


class BaseParser:
    MONTH_DICT = {
        "январь": 1, "января": 1,
        "февраль": 2, "февраля": 2,
        "март": 3, "марта": 3,
        "апрель": 4, "апреля": 4,
        "май": 5, "мая": 5,
        "июнь": 6, "июня": 6,
        "июль": 7, "июля": 7,
        "август": 8, "августа": 8,
        "сентябрь": 9, "сентября": 9,
        "октябрь": 10, "октября": 10,
        "ноябрь": 11, "ноября": 11,
        "декабрь": 12, "декабря": 12
    }

    HEADERS = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/94.0.4606.81 Safari/537.36",
        "accept": "*/*",
    }

    @staticmethod
    def safe_url(link: str) -> str:
        url = link.strip()
        return url

    def get_html(self, link: str) -> Optional[httpx.Response]:
        url = self.safe_url(link)
        headers = self.HEADERS
        try:
            response = httpx.get(url, headers = headers)
            if response.status_code == 200:
                return response
            logging.info(response.status_code)
        except (httpx.ConnectError, httpx.ConnectTimeout) as err:
            logging.error(err.__doc__)
            return


class UniversalParser(BaseParser):
    def get_date(self, text: str) -> datetime:
        date_regex = [
            (
                r'(\d{2}) ([а-я]*) (\d{4})',
                lambda x: datetime(
                    int(x.group(3)),
                    self.MONTH_DICT.get(x.group(2).lower()),
                    int(x.group(1)))
            ),
            (
                r'(\d{2})\.(\d{2}).(\d{4})',
                lambda x: datetime(
                    int(x.group(3)),
                    int(x.group(2)),
                    int(x.group(1)))
            ),
            (
                r'(\d{4})\.(\d{2}).(\d{2})',
                lambda x: datetime(
                    int(x.group(1)),
                    int(x.group(2)),
                    int(x.group(3)))
            ),
            (
                r'(\d{2})/(\d{2})/(\d{4})',
                lambda x: datetime(
                    int(x.group(3)),
                    int(x.group(2)),
                    int(x.group(1)))
            ),
            (
                r'(\d{4})/(\d{2})/(\d{2})',
                lambda x: datetime(
                    int(x.group(1)),
                    int(x.group(2)),
                    int(x.group(3)))
            )
        ]
        for item in date_regex:
            dt = re.search(item[0], text)
            if dt:
                date = item[1](dt)
                return date

    def parse_html(self, url: str) -> dict:
        html = self.get_html(url)
        if html:
            soup = BeautifulSoup(html, 'lxml')
            title = soup.find('title').get_text()
            body = soup.find('body')
            text_list = []
            count = 0
            for string in body.stripped_strings:
                if count == 150:
                    break
                if len(string) > 7:
                    if 'https' not in string and '@' not in string:
                        if string not in text_list:
                            text_list.append(string.replace('\xa0', ' '))
                            count += 1
            text = ''
            for string in text_list:
                text += f"{string} "
            date = self.get_date(title)
            if not date:
                date = self.get_date(text)
            if not date:
                date = datetime.now(pytz.utc)
            return {"date": date, "title": title, "url": url, "text": text}


class AbstractParserNews(BaseParser, ABC):
    HOST = ''
    DATE_FORMAT = ''

    def get_date_today(self) -> str:
        dt = datetime.today().date()
        date = dt.strftime(self.DATE_FORMAT)
        return date

    def get_url_news_list(self) -> str:
        url = f"{self.HOST}{self.get_date_today()}"
        return url

    @abstractmethod
    def get_news_list(self) -> List[dict]:
        pass

    @abstractmethod
    def get_news_text(self, url: str) -> dict:
        pass


class SputnikParserNews(AbstractParserNews):
    HOST = 'https://sputnik.by'
    DATE_FORMAT = '/%Y%m%d/'

    def get_news_list(self) -> list:
        url = self.get_url_news_list()
        html = self.get_html(url)
        if html:
            soup = BeautifulSoup(html, 'lxml')
            items = soup.find_all('a', class_='list__title')
            date_time = datetime.now(pytz.utc)
            news_list = []
            for item in items:
                news_list.append(
                    {
                        "date": date_time,
                        "title": item.get("title"),
                        "url": self.HOST + item.get("href")
                    }
                )
            return news_list

    def get_news_text(self, url: str) -> dict:
        html = self.get_html(url)
        if html:
            soup = BeautifulSoup(html, 'lxml')
            body = soup.find_all('div', class_ = 'article__text')
            date = soup.find('div', class_ = 'article__info-date').get_text(strip = True)
            dt = re.search(r'(\d{2})\.(\d{2}).(\d{4})', date).group(0)
            tm = re.search(r'(\d{2}):(\d{2})', date).group(0)
            dt_tm = f"{tm} {dt}"
            date_time = datetime.strptime(dt_tm, '%H:%M %d.%m.%Y')
            preview = soup.find('div', class_ = 'article__announce-text').get_text()
            text = f"{preview} "
            for item in body:
                text += item.get_text().replace('.', '. ')
            news = {"date": date_time, "text": text.strip()}
            return news


class LentaParserNews(AbstractParserNews):
    HOST = 'https://lenta.ru'
    DATE_FORMAT = '/%Y/%m/%d/'

    def get_url_news_list(self):
        url = f"{self.HOST}/news{self.get_date_today()}"
        return url

    def get_news_list(self) -> Union[list, dict]:
        url = self.get_url_news_list()
        html = self.get_html(url)
        if html:
            soup = BeautifulSoup(html, 'lxml')
            items = soup.find_all('a', class_ = 'titles')
            date_time = datetime.now(pytz.utc)
            news_list = []
            for item in items:
                title = str(item.find('h3', class_ = 'card-title').get_text())
                news_list.append(
                    {
                        "date": date_time,
                        "title": title.replace('\xa0', ' '),
                        "url": self.HOST + item.get('href')
                    }
                )
            return news_list

    def get_news_text(self, url: str) -> dict:
        html = self.get_html(url)
        if html:
            soup = BeautifulSoup(html, 'lxml')
            body = soup.find('div', class_ = 'b-text clearfix js-topic__text').get_text()
            date = soup.find('div', class_ = 'b-topic__info').get_text(strip = True)
            dt = re.search(r'(\d{2}) ([а-я]*) (\d{4})', date)
            tm = re.search(r'(\d{2}):(\d{2})', date)
            date_time = datetime(
                int(dt.group(3)),
                self.MONTH_DICT.get(dt.group(2).lower()),
                int(dt.group(1)),
                int(tm.group(1)),
                int(tm.group(2))
            )
            preview = soup.find('div', class_ = 'b-topic__title-yandex').get_text()
            text = f"{preview}. {body}"
            news_text = {"date": date_time, "text": text}
            return news_text


class EuronewsParserNews(AbstractParserNews):
    HOST = 'https://ru.euronews.com'
    DATE_FORMAT = '/%Y/%m/%d/'

    def get_news_list(self) -> Union[dict, list]:
        url = self.get_url_news_list()
        html = self.get_html(url)
        if html:
            soup = BeautifulSoup(html, 'lxml')
            items = soup.find_all('a', class_ = 'm-object__title__link')
            date_time = datetime.now(pytz.utc)
            news_list = []
            for item in items:
                news_list.append(
                    {
                        "date": date_time,
                        "title": item.get('title'),
                        "url": self.HOST + item.get('href')
                    }
                )
            return news_list

    def get_news_text(self, url: str) -> dict:
        html = self.get_html(url)
        if html:
            soup = BeautifulSoup(html, 'lxml')
            date = soup.find('time').get_text()
            dt = re.search(r'\d{2}/\d{2}/\d{4}', date).group(0)
            try:
                tm = re.search(r'\d{2}:\d{2}', date).group(0)
            except AttributeError:
                tm = '00:00'
            dt_tm = f"{dt} {tm}"
            date_time = datetime.strptime(dt_tm, '%d/%m/%Y %H:%M')
            body = soup.find_all('div', class_ = 'c-article-content js-article-content')
            if not body:
                body = soup.find_all('div', class_ = 'c-article-content')
            text = ''
            for item in body:
                text = item.get_text().replace('.', '. ')
            news_text = {"date": date_time, "text": text.strip()}
            return news_text
