# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class MeishichinaItem(Item):
    classification = Field() #美食分类
    src = Field() #美食图片路径
    msname = Field() #美食名称
    material = Field() #原料
    step = Field() #步骤和每步的图片路径 存入json数组，


