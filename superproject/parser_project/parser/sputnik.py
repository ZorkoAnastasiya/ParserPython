import re
import pytz
from datetime import datetime
from bs4 import BeautifulSoup
from typing import Optional
from parser_project.parser.base import AbstractParserNews, ParserTypeList, ParserTypeText


class SputnikParserNews(AbstractParserNews):
    """
    Parsing the list of news and news articles from the site sputnik.by.
    """
    HOST = 'https://sputnik.by'
    DATE_FORMAT = '/%Y%m%d/'

    def get_news_list(self) -> Optional[ParserTypeList]:
        """
        Getting a list of news for the current date.
        """
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

    def get_news_text(self, url: str) -> Optional[ParserTypeText]:
        """
        Receiving a news article.
        """
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
