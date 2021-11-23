import json
import re
from datetime import datetime
from json import JSONDecodeError
from typing import Any
from typing import Callable
from typing import List
from typing import Optional
from typing import Tuple

import pytz
from bs4 import BeautifulSoup
from devtools import debug

from parser_project.parser.base import BaseParser
from parser_project.parser.base import ParserTypeText


class UniversalParser(BaseParser):
    """
    Searches for the title, text and date of any HTML page.
    """

    def get_date(self, text: str) -> Optional[datetime]:
        """
        Searches for a date in the text and, if found, converts it to a datetime object.
        """
        result: Optional[datetime] = None
        date_regex: List[Tuple[str, Callable]] = [
            (
                r"(\d{2})[./](\d{2})[./](\d{4})",
                lambda x: datetime(
                    int(x.group(3)),
                    int(x.group(2)),
                    int(x.group(1)),
                ),
            ),
            (
                r"(\d{4})[./](\d{2})[./](\d{2})",
                lambda x: datetime(
                    int(x.group(1)),
                    int(x.group(2)),
                    int(x.group(3)),
                ),
            ),
            (
                r"(\d{1,2})\s+([а-я]*)\s+(\d{4})",
                lambda x: datetime(
                    int(x.group(3)),
                    self.MONTH_DICT.get(x.group(2).lower()),  # type: ignore
                    int(x.group(1)),
                ),
            ),
        ]
        for item in date_regex:
            date: Any = re.search(item[0], text)
            if date:
                try:
                    result = item[1](date)
                except (ValueError, TypeError) as err:
                    error = f"Completed with error: {err.__doc__} {err}. Date: {date}"
                    debug(error)
        return result

    def parse_html(self, url: str) -> Optional[ParserTypeText]:
        """
        Parses the HTML page.
        """
        result: Optional[ParserTypeText] = None
        html = self.get_html(url)
        if html:
            soup = BeautifulSoup(html, "lxml")
            try:
                title = soup.find("title").get_text()
                body = soup.find("body")
                text_list = []
                count = 0
                for string in body.stripped_strings:
                    if count == 200:
                        break
                    if len(string) > 7:
                        if "https" not in string and "@" not in string:
                            if string not in text_list:
                                text_list.append(string.replace("\xa0", " "))
                                count += 1
                text = ""
                for string in text_list:
                    text += f"{string} "
                date = self.get_date(title)
                if not date:
                    date = self.get_date(text)
                if not date:
                    date = datetime.now(pytz.utc)
                result = {
                    "date": date,
                    "title": title,
                    "url": url,
                    "text": text,
                }

            except AttributeError as err:
                error = f"Completed with AttributeError, trying to find JSON."
                debug(error)

                try:
                    body = soup.find("body")
                    text = json.loads(body.text)
                    date = datetime.now(pytz.utc)
                    title = f"JSON object: {url}"
                    result = {
                        "date": date,
                        "title": title,
                        "url": url,
                        "text": text,
                    }

                except JSONDecodeError as err:
                    error = f"Completed with error: {err.__doc__} {err}"
                    debug(error)
        return result
