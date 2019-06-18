# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YunjiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    parent_category = scrapy.Field()
    category = scrapy.Field()
    aid = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    vprice = scrapy.Field()
    brand = scrapy.Field()
    oss_imgpath_list = scrapy.Field()
    oss_imagepath_list = scrapy.Field()
    oss_parameters = scrapy.Field()
    parameters = scrapy.Field()


