import re
import pytz
from datetime import datetime
from bs4 import BeautifulSoup
from parser_project.parser.base import BaseParser


class UniversalParser(BaseParser):

    def get_date(self, text: str) -> datetime:
        date_regex = [
            (
                r'(\d{1,2})\s+([а-я]*)\s+(\d{4})',
                lambda x: datetime(
                    int(x.group(3)),
                    self.MONTH_DICT.get(x.group(2).lower()),
                    int(x.group(1)),
                )
            ),
            (
                r'(\d{2})[./](\d{2})[./](\d{4})',
                lambda x: datetime(
                    int(x.group(3)),
                    int(x.group(2)),
                    int(x.group(1)),
                )
            ),
            (
                r'(\d{4})[./](\d{2})[./](\d{2})',
                lambda x: datetime(
                    int(x.group(1)),
                    int(x.group(2)),
                    int(x.group(3)),
                )
            ),
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
            date = self.get_date(title)
            if not date:
                date = self.get_date(text)
            if not date:
                date = datetime.now(pytz.utc)
            return {"date": date, "title": title, "url": url, "text": text}
