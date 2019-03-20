# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TaobaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 商品类别
    cid = scrapy.Field()
    # 商品名称
    title = scrapy.Field()
    # 商品比率值
    tkRate = scrapy.Field()
    # 详情页面的URL地址
    auctionUrl = scrapy.Field()
    # 商品的发货地址
    deliveryAdd = scrapy.Field()
    # 商品的价格
    price = scrapy.Field()
    # 产品参数
    comm_data = scrapy.Field()
    # 商品ID
    comm_id = scrapy.Field()
    # oss上的主图的URL地址
    oss_imgurl = scrapy.Field()
    # oss上的详情图的URL地址
    oss_imageurl = scrapy.Field()

