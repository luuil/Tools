import scrapy
import urllib
import json
from pypinyin import lazy_pinyin
from scrapy.loader import ItemLoader 
from gokskill.items import ImageItem

class RosiSpider(scrapy.Spider):
    name = "gok"
    allowed_domains = ['pvp.qq.com']
    start_urls = [
        # 'http://pvp.qq.com/',
    ]
    start_json_url = 'http://pvp.qq.com/web201605/js/herolist.json'
    gok_url_base = 'http://pvp.qq.com/web201605/herodetail/'
    hero_dict = {
        # 180 : 'AnQiLa'
    }

    def start_requests(self):
        self.set_start_urls()
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse,
                                    errback=self.errback,
                                    dont_filter=True)


    def parse(self, response):
        yield self.parse_item(response) # ok
        for a in response.css('a::attr(href)').extract():
            if not a:
                continue
            next_page = response.urljoin(a)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_item(self, response):
        il = ItemLoader(item=ImageItem(), response=response)
        il.add_css('image_urls', 'img::attr(src)') # get all image url
        il.add_value('hero_dict', self.hero_dict)
        return il.load_item()

    def errback(self, failure):
        pass

    def set_start_urls(self):
        response = urllib.request.urlopen(self.start_json_url)
        data = json.load(response)
        for hero in data:
            # http://pvp.qq.com/web201605/herodetail/180.shtml
            hero_url = self.gok_url_base + str(hero['ename']) + '.shtml'
            hero_no = hero['ename']
            hero_name = ''.join(name.capitalize() for name in lazy_pinyin(hero['cname']))
            self.hero_dict[hero_no]=hero_name
            self.start_urls.append(hero_url)
        # print self.hero_dict
        # print self.start_urls

