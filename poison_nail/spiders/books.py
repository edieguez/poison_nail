from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


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
            yield {
                'name': book.css('h3 a::attr(title)').get(),
                'price': book.css('div.product_price p.price_color::text').get(),
                'image': response.urljoin(book.css('div.image_container img::attr(src)').get()),
            }
