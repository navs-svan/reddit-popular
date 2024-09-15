import scrapy


class RedspiderSpider(scrapy.Spider):
    name = "redspider"
    allowed_domains = ["old.reddit.com"]

    def __init__(self, country="PH", *args, **kwargs):
        super(RedspiderSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f"https://old.reddit.com/r/popular/?geo_filter={country}"]

    def parse(self, response):
        posts = response.css("#siteTable :not(.promoted):has(div.entry.unvoted)")
        for post in posts:
            yield {"url": post.css("div::attr(data-permalink)").get()}

        # NEXT PAGE
        next_page = response.css(".next-button a::attr(href)").get()
        yield response.follow(next_page, callback=self.parse)
