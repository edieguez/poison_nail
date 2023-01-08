# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


def remove_currency(value):
    return value.replace('£', '')


def get_full_link(url, loader_context):
    response = loader_context.get('response')
    return response.urljoin(url)


class BookItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(remove_currency), output_processor=TakeFirst())
    image = scrapy.Field(input_processor=MapCompose(get_full_link), output_processor=TakeFirst())


class QuoteItem(scrapy.Item):
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
