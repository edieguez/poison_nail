from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule

from poison_nail.items import BookItem


class BooksSpider(CrawlSpider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com']
    rules = (
        Rule(LinkExtractor(allow=r'catalogue/page-\d+\.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        books = response.css('article.product_pod')

        for book in books:
            item_loader = ItemLoader(BookItem(), book, response)

            item_loader.add_css('name', 'h3 > a::attr(title)')
            item_loader.add_css('price', 'div.product_price > p.price_color::text')
            item_loader.add_css('image', 'div.image_container > a > img::attr(src)')

            yield item_loader.load_item()
