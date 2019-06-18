# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YelpItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    # 详情页面URL
    detail_page_url = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 名称
    name = scrapy.Field()
    # 街道
    street = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 电话
    tel = scrapy.Field()
    # 类别
    forms = scrapy.Field()
    # 邮箱
    email = scrapy.Field()
    # logo图片链接
    logo_imgurl = scrapy.Field()
    # 背景图
    back_img = scrapy.Field()
    # 经纬度
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    # 描述
    description = scrapy.Field()
