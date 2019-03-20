# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ToutiaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    writer = scrapy.Field()
    publish_time = scrapy.Field()
    article = scrapy.Field()
    tags = scrapy.Field()
    class_id = scrapy.Field()
    read_number= scrapy.Field()
    summary= scrapy.Field()
    article_id = scrapy.Field()
    oss_url1 = scrapy.Field()
