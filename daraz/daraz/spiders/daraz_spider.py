import scrapy
import json
import re
import ipdb


class DarazSpider(scrapy.Spider):
    name = "daraz"
    page = 1
    text = ''
    count = 0
    data = []

    def start_requests(self):
        self.text = input("Text to Search: ").strip().replace(" ", "-")
        url = f"https://www.daraz.com.np/catalog/?q={self.text}"
        yield scrapy.Request(url=url, callback=self.parse, meta={"proxy": "https://91.214.128.243:23500"})

    def parse(self, response):
        with open("index.html", "wb") as f:
            f.write(response.body)
        script_list = response.css("script::text").getall()
        data = list(filter(
            lambda x: True if 'window.pageData=' in x else False, script_list))
        try:
            data = json.loads(data[0].replace("window.pageData=", ""))
        except:
            pass
        products = data['mods']['listItems']
        data_to_print = []
        for i, product in enumerate(products):
            self.count = self.count + 1
            data = {
                'id': self.count,
                'page': self.page,
                'name': product['name'],
                'productUrl': product['productUrl'],
                'image': product['image'],
                "price": product['price'],
            }
            self.data.append(data)
            yield data
        print(f"page {self.page} completed")
        next_page = response.css(
            "head > link[rel='next']::attr(href)").getall()

        if(next_page):
            next_page = next_page[0] + f"&q={self.text}"
            page = re.sub(r'.+\?', "", next_page).split("&")
            page = list(
                filter(lambda x: True if 'page=' in x else False, page))[0].replace("page=", "")
            self.page = int(page)
            yield response.follow(next_page, self.parse)
        else:
            with open("Data/"+self.text+'.json', 'a+') as f:
                json.dump(self.data, f)
