# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JingdongItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 详情页面的URL地址

    cid = scrapy.Field()
    comm_id = scrapy.Field()
    title = scrapy.Field()
    auctionUrl = scrapy.Field()
    price = scrapy.Field()
    brand = scrapy.Field()
    comm_attr = scrapy.Field()
    oss_imgurl = scrapy.Field()
    oss_imageurl= scrapy.Field()
    discount_price = scrapy.Field()

