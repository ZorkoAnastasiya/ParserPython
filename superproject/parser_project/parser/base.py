import httpx
from devtools import debug
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, List, Dict, Union

ParserTypeList = List[Dict[str, Union[datetime, str]]]
ParserTypeText = Dict[str, Union[datetime, str]]


class BaseParser:
    """
    Helper class for creating parsers.
    Requests Html pages.
    Contains a dictionary for converting the month name to numbers.
    """

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
        """
        It takes an url as a parameter and sends a request to the specified path.
        Returns:
        httpx.response if the status code is 200;
        None if an error occurs or the status code is not 200
        """
        headers = self.HEADERS
        try:
            response = httpx.get(url, headers = headers)
            if response.status_code == 200:
                return response
            res = f'Completed with code: {response.status_code}'
            debug(res)
        except (httpx.ConnectError, httpx.ConnectTimeout) as err:
            debug(f'Work completed with error: {err}')
            return


class AbstractParserNews(BaseParser, ABC):
    """
    Helper class for creating news parsers.
    """

    HOST = ''
    DATE_FORMAT = ''

    def get_date_today(self) -> str:
        """
        Retrieves the current date and converts it to a string in the specified format.
        """
        dt = datetime.today().date()
        date = dt.strftime(self.DATE_FORMAT)
        return date

    def get_url_news_list(self) -> str:
        """
        Creates a link by concatenating hostname and date format.
        """
        url = f"{self.HOST}{self.get_date_today()}"
        return url

    @abstractmethod
    def get_news_list(self) -> Optional[ParserTypeList]:
        """
        Getting a list of news.
        """
        pass

    @abstractmethod
    def get_news_text(self, url: str) -> Optional[ParserTypeText]:
        """
        Receiving news text.
        """
        pass
