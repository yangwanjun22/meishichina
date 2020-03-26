# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
#coding=utf-8
from scrapy.spiders import Spider
from scrapy.http import Request
from ..items import MeishichinaItem
from bs4 import BeautifulSoup
import logging
import json
from ..MyEncoder import MyEncoder

class MeishichinaSpider(Spider):
    name = "meishichina"
    allow_domain = ["home.meishichina.com"]
    start_urls = ["https://home.meishichina.com/recipe-type.html"]

    #每类美食对应的url
    def parse(self, response):
        class_links = set(response.css('div.category_sub.clear a::attr(href)').extract())
        #class_links = {'https://home.meishichina.com/recipe/recai/page/1991/'}
        for link in class_links:
            yield Request(url = link, callback = self.parse_detail)

    #每类中所有url(每种美食url)  需要分页 获取页数
    def parse_detail(self, response):
        name_links = set(response.css('div.pic a::attr(href)').extract())

        #提取下一页
        nextnode = response.css('a.now_page + a').extract()
        print(nextnode)
        if nextnode != []:
            next_url = response.css('a.now_page + a::attr(href)').extract()[0]
            next_url = response.urljoin(next_url)
            #构造新的Request对象
            yield Request(url = next_url, callback = self.parse_detail)

        for link in name_links:
            yield Request(url=link, callback=self.parse_feed)

    #处理每种美食
    def parse_feed(self, response):
        rss = BeautifulSoup(response.body, 'lxml')
        classification = response.css('div.clear>span+a::text').extract() #类别
        src = response.css('a.J_photo img::attr(src)').extract()[0] #美食图片路径
        name = response.css('input#recipe_title::attr(value)').extract()[0] #美食名称
        material = response.css('.category_s1 b::text').extract() #美食原料
        stepsrc = response.css('div.recipeStep_img img::attr(src)').extract() #步骤图片
        step = response.css('div.recipeStep_word::text').extract() #步骤操作

        #处理数据
        classification1 = ""
        material1=""

        for c in classification:
            classification1 = classification1 + "/" + c;
        classification1 = classification1[1:]

        for m in material:
            material1 = material1 + "," + m
        material1 = material1[1:]

        steps = [];
        for index in range(len(step)):
            substep = {'src': stepsrc[index], 'operate': step[index] }
            steps.append(substep)
        step1 = json.dumps(steps,ensure_ascii=False)

        feed_item = MeishichinaItem()
        feed_item['classification'] = classification1
        feed_item['src'] = src
        feed_item['msname'] = name
        feed_item['material'] = material1
        feed_item['step'] = step1
        yield feed_item




