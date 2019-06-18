# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZillowItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 详情页URL
    aurl = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 卧室
    room = scrapy.Field()
    # 浴室
    bath = scrapy.Field()
    # 活动面积
    living_area = scrapy.Field()
    # 地址
    addres = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 州
    state = scrapy.Field()
    # 邮编
    postcode = scrapy.Field()
    # 租赁类型
    rent = scrapy.Field()
    # 时间
    days = scrapy.Field()
    # 房屋类型
    type_room = scrapy.Field()
    # 建造年份
    year_built = scrapy.Field()
    # 停车场
    parking = scrapy.Field()
    # 居住面积
    lot = scrapy.Field()
    # 图片URL
    img_url = scrapy.Field()
    # 联系人
    name = scrapy.Field()
    # 联系方式
    phone = scrapy.Field()


