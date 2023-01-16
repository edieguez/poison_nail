from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from poison_nail.items import QuoteItem


class QuotesSpider(CrawlSpider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com']
    rules = (
        Rule(LinkExtractor(allow=r'/page/\d+/', deny='/tag'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        for quote in response.css('div.quote'):
            quote_item = QuoteItem()
            quote_item['text'] = quote.css('span.text::text').get()
            quote_item['author'] = quote.css('small.author::text').get()
            quote_item['tags'] = quote.css('div.tags a.tag::text').getall()

            yield quote_item
