from typing import Any

from django.shortcuts import get_object_or_404

from parser_project.models import Articles
from parser_project.models import Resources
from parser_project.parser.base import ParserTypeList
from parser_project.parser.base import ParserTypeText
from parser_project.parser.euronews import EuronewsParserNews
from parser_project.parser.lenta import LentaParserNews
from parser_project.parser.sputnik import SputnikParserNews


class ParserMixin:
    """
    Calls parsers and their methods.
    Saves data obtained as a result of the work of parsers.
    """

    model = Articles

    @staticmethod
    def get_parser(resource: str) -> Any:
        """
        Selects a suitable parser.
        """
        if resource == "Другие ресурсы":
            return None
        elif resource == "Sputnik Беларусь":
            return SputnikParserNews()
        elif resource == "Lenta Новости":
            return LentaParserNews()
        elif resource == "Euronews":
            return EuronewsParserNews()

    def save_data_list(self, news_list: ParserTypeList, pk: int) -> None:
        """
        Saves the received news headlines,
        links to articles and the resource from which they were retrieved.
        Saves the current date as "article date".
        """
        for item in news_list:
            if not self.model.objects.filter(url=item["url"]).exists():
                self.model.objects.create(
                    date=item["date"],
                    title=item["title"],
                    url=item["url"],
                    resource_id=pk,
                )

    def save_data_text(self, text: ParserTypeText, pk: int) -> None:
        """
        Saves the text of the article and updates the date the article was written.
        """
        obj = self.model.objects.get(id=pk)
        obj.date = text["date"]
        obj.text = text["text"]
        obj.save()

    def parse_news_list(self, pk: int) -> None:
        """
        Parses the HTML page with a list of news for the current date.
        """
        obj = get_object_or_404(Resources, id=pk)
        parser = self.get_parser(str(obj.title))
        if parser:
            news_list = parser.get_news_list()
            if news_list:
                self.save_data_list(news_list, pk)

    def parse_text(self, obj: Articles) -> None:
        """
        Parses the HTML page with the news text.
        """
        parser = self.get_parser(str(obj.resource.title))
        if parser:
            text = parser.get_news_text(obj.url)
            if text:
                self.save_data_text(text, obj.pk)
