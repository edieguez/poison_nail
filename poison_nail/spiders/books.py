import scrapy


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com']

    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:
            yield {
                'name': book.css('h3 a::attr(title)').get(),
                'price' : book.css('div.product_price p.price_color::text').get(),
                'image' : response.urljoin(book.css('div.image_container img::attr(src)').get()),
            }
