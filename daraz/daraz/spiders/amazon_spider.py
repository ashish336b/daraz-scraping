import scrapy
import json


class DarazSpider(scrapy.Spider):
    name = "daraz"
    page = 1
    text = ''

    def start_requests(self):
        self.text = input("Text to Search: ").strip().replace(" ", "-")
        url = f"https://www.daraz.com.np/catalog/?q={self.text}&sort=pricedesc"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        pass
