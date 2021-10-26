import re
import pytz
from typing import Union
from datetime import datetime
from bs4 import BeautifulSoup
from parser_project.parser.base import AbstractParserNews


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
