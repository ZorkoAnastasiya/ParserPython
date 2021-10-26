import httpx
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, List


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

    def get_html(self, url: str) -> Optional[httpx.Response]:
        headers = self.HEADERS
        try:
            response = httpx.get(url, headers = headers)
            if response.status_code == 200:
                return response
            logging.info(response.status_code)
        except (httpx.ConnectError, httpx.ConnectTimeout) as err:
            logging.error(err.__doc__)
            return


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
