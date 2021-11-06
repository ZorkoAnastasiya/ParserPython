import re
from datetime import datetime
from typing import Any
from typing import Optional

import pytz
from bs4 import BeautifulSoup

from parser_project.parser.base import AbstractParserNews
from parser_project.parser.base import ParserTypeList
from parser_project.parser.base import ParserTypeText


class LentaParserNews(AbstractParserNews):
    """
    Parsing the list of news and news articles from the site lenta.ru.
    """

    HOST = "https://lenta.ru"
    DATE_FORMAT = "/%Y/%m/%d/"

    def get_url_news_list(self) -> str:
        """
        Overriding the parent method to generate the correct link.
        """
        url = f"{self.HOST}/news{self.get_date_today()}"
        return url

    def get_news_list(self) -> Optional[ParserTypeList]:
        """
        Getting a list of news for the current date.
        """
        result: Optional[ParserTypeList] = None
        url = self.get_url_news_list()
        html = self.get_html(url)
        if html:
            soup = BeautifulSoup(html, "lxml")
            items = soup.find_all("a", class_="titles")
            date_time = datetime.now(pytz.utc)
            news_list = []
            for item in items:
                title = str(item.find("h3", class_="card-title").get_text())
                news_list.append(
                    {
                        "date": date_time,
                        "title": title.replace("\xa0", " "),
                        "url": self.HOST + item.get("href"),
                    }
                )
            result = news_list
        return result

    def get_news_text(self, url: str) -> Optional[ParserTypeText]:
        """
        Receiving a news article.
        """
        result: Optional[ParserTypeText] = None
        html = self.get_html(url)
        if html:
            soup = BeautifulSoup(html, "lxml")
            body = soup.find(
                "div", class_="b-text clearfix js-topic__text"
            ).get_text()
            date = soup.find("div", class_="b-topic__info").get_text(
                strip=True
            )
            dt: Any = re.search(r"(\d{1,2})\s+([а-я]*)\s+(\d{4})", date)
            tm: Any = re.search(r"(\d{2}):(\d{2})", date)
            date_time = datetime(
                int(dt.group(3)),
                self.MONTH_DICT.get(dt.group(2).lower()),  # type: ignore
                int(dt.group(1)),
                int(tm.group(1)),
                int(tm.group(2)),
            )
            preview = soup.find(
                "div", class_="b-topic__title-yandex"
            ).get_text()
            text = f"{preview}. {body}"
            news_text = {"date": date_time, "text": text}
            result = news_text
        return result
