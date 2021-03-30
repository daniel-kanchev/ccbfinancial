import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from ccbfinancial.items import Article


class ccbfinancialSpider(scrapy.Spider):
    name = 'ccbfinancial'
    start_urls = ['https://www.ccbfinancial.com/Publications/CCB']

    def parse(self, response):
        links = response.xpath('//div[@class="col-sm-12 col-md-6 pub_content bottom-pad-40"]/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h3[@class="blue"]/text()').get()
        if title:
            title = title.strip()

        content = response.xpath('//div[@id="pubContentView"]//text()').getall()
        content = [text for text in content if text.strip() and '{' not in text]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
