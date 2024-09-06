import scrapy


class RedspiderSpider(scrapy.Spider):
    name = "redspider"
    allowed_domains = ["reddit.com"]
    start_urls = ["https://reddit.com"]

    def parse(self, response):
        pass
