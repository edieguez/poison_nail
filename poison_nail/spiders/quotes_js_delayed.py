import scrapy
from scrapy_playwright.page import PageMethod

import poison_nail.settings
from poison_nail.items import QuoteItem


class QuotesJsDelayedSpider(scrapy.Spider):
    name = 'quotes-js-delayed'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['https://quotes.toscrape.com/js-delayed']
    custom_settings = poison_nail.settings.PLAYWRIGHT_SETTINGS

    def start_requests(self):
        for url in self.start_urls:
            yield self._send_request(url)

    async def parse(self, response, **kwargs):
        page = response.meta['playwright_page']
        await page.close()

        for quote in response.css('div.quote'):
            quote_item = QuoteItem()
            quote_item['text'] = quote.css('span.text::text').get()
            quote_item['author'] = quote.css('small.author::text').get()
            quote_item['tags'] = quote.css('div.tags a.tag::text').getall()

            yield quote_item

        next_page = response.css('.next>a ::attr(href)').get()

        if next_page:
            next_page_url = response.urljoin(next_page)
            yield self._send_request(next_page_url)

    def _send_request(self, url):
        return scrapy.Request(url, meta={
            'playwright': True,
            'playwright_include_page': True,
            'playwright_page_methods': [
                PageMethod('wait_for_selector', 'div.quote'),
            ],
            'errback': self.errback,
        })

    async def errback(self, failure):
        page = failure.request.meta['playwright_page']
        await page.close()
