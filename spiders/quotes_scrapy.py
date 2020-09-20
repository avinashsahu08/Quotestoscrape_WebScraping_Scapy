import scrapy
from ..items import QuotetutorialItem
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser


class QuoteSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com/login']

    def parse(self, response):
        token = response.css('form input::attr(value)').extract_first()

        return FormRequest.from_response(response, formdata={
            'csrf_token': token,
            'username': 'abcd',
            'password': 'abcd'
        }, callback=self.start_scraping)

    def start_scraping(self, response):
        #open_in_browser(response)
        items = QuotetutorialItem()
        all_div_quotes = response.css('div.quote')

        for quotes in all_div_quotes:
            title = quotes.css('span.text::text').extract()
            author = quotes.css('.author::text').extract()
            tag = quotes.css('.tag::text').extract()

            items['title'] = title
            items['author'] = author
            items['tag'] = tag

            yield items  # using yield with containers

        # extracting data of all the pages and not just 1st page
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.start_scraping)
