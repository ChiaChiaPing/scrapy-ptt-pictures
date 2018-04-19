# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader
from ptt.items import PttItem

i=1
class PtSpider(scrapy.Spider):
    name = 'pt'
    allowed_domains = ['www.ptt.cc']
    # 針對 start_urls：他會在後面自動加 index.html
    #start_urls = ['https://www.ptt.cc/bbs/Beauty/']
    pages=0

    def __init__(self):
        self.pages=input("要收集幾頁的資料：")
        self.start_urls=["https://www.ptt.cc/bbs/Beauty/"]

    def parse(self, response):
        post=response.xpath("//*[@class='title']/a[contains(text(),'正妹')]/@href").extract()
        for po in post:
            url=response.urljoin(po)
            yield Request(url,callback=self.parse_post)

        while i<=pages:# 決定頁數
            next_=response.xpath("//*[@class='btn wide' and text()='上頁 ›']/@href").extract_first()
            next_=response.urljoin(next_)
            i+=1
            yield Request(next_,callback=self.parse,dont_filter=True)

    def parse_post(self,response):
        images=response.xpath("//*[contains(@href,'i.imgur')]/@href").extract()
        l=ItemLoader(item=PttItem(),response=response)
        for im in images:
            l.add_value("image_urls",im) # 感覺有點像是append到後面的感覺
            #yield l.load_item()
        yield l.load_item()
