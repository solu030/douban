import scrapy

from scrapy import Request

from douban.items import DoubanItem

class MoviespiderSpider(scrapy.Spider):
    name = "movieSpider"
    allowed_domains = ["movie.douban.com"]
    # start_urls = ["https://movie.douban.com/top250"]
    def start_requests(self):
        for page in range(2):
            yield scrapy.Request(f"https://movie.douban.com/top250?start={page * 25}&filter=")

    def parse(self, response):
        sel = scrapy.Selector(response)
        list_items = sel.css('#content > div > div.article > ol > li')
        for list_item in list_items:
            movie_obj = DoubanItem()
            detail_url = list_item.css('div.info > div.hd > a::attr(href)').get()
            movie_obj["title"] = list_item.css('span.title::text').get()
            movie_obj["score"] = list_item.css('span.rating_num::text').get()
            movie_obj["subject"] = list_item.css('span.inq::text').get()
            yield Request(url=detail_url,callback=self.detail_parse,cb_kwargs={"obj":movie_obj})

    def detail_parse(self,response,**kwargs):
        movie_obj = kwargs['obj']
        sel = scrapy.Selector(response)
        movie_obj["duration"] = sel.css('span[property="v:runtime"]::attr(content)').get()
        yield movie_obj
