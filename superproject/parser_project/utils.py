from typing import Union
from parser_project.models import Resources, Articles
from parser_project.parser.euronews import EuronewsParserNews
from parser_project.parser.lenta import LentaParserNews
from parser_project.parser.sputnik import SputnikParserNews


class ParserMixin:
    model = Articles

    @staticmethod
    def get_parser(resource: str) -> Union[
        SputnikParserNews,
        LentaParserNews,
        EuronewsParserNews,
        None
    ]:
        if resource == 'Другие ресурсы':
            return
        elif resource == 'Sputnik Беларусь':
            return SputnikParserNews()
        elif resource == 'Lenta Новости':
            return LentaParserNews()
        elif resource == 'Euronews':
            return EuronewsParserNews()

    def save_data_list(self, news_list: list, pk: int) -> None:
        for item in news_list:
            if not self.model.objects.filter(url = item['url']).exists():
                self.model.objects.create(
                    date = item['date'],
                    title = item['title'],
                    url = item['url'],
                    resource_id = pk
                )

    def save_data_text(self, text: dict, pk: int) -> None:
        obj = self.model.objects.get(id = pk)
        obj.date = text['date']
        obj.text = text['text']
        obj.save()

    def parse_news_list(self, pk: int)-> Union[list, int, None]:
        obj = Resources.objects.get(id = pk)
        parser = self.get_parser(str(obj.title))
        if parser:
            news_list = parser.get_news_list()
            if news_list:
                return self.save_data_list(news_list, pk)

    def parse_text(self, obj) -> Union[dict, int, None]:
        parser = self.get_parser(str(obj.resource.title))
        if parser:
            url = obj.url
            text = parser.get_news_text(url)
            if text:
                return self.save_data_text(text, obj.id)
