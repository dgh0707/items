# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

class ZillowPipeline(object):
    # def __init__(self):
    #     # 测试数据库
    #     self.conn = pymysql.connect(user='root', passwd='2018@Amber123', db='apst_share',
    #                                 host='47.93.244.121', charset='utf8')
    #     self.cursor = self.conn.cursor()
    def process_item(self, item, spider):
        # tit = self.cursor.execute('select id from zillow where aurl=%s', (item['aurl']))
        # if tit:
        #
        #     tit = self.cursor.fetchone()
        # else:
        #     self.cursor.execute(
        #         """INSERT INTO zillow (aurl,price,room,bath,living_area,addres,city,state,postcode,rent,days,type_room,year_built,parking,lot)VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")""" %
        #         (
        #             item['aurl'],
        #             item['price'],
        #             item['room'],
        #             item['bath'],
        #             pymysql.escape_string(item['living_area']),
        #             item['addres'],
        #             item['city'],
        #             pymysql.escape_string(item['state']),
        #             item['postcode'],
        #             item['rent'],
        #             item['days'],
        #             item['type_room'],
        #             item['year_built'],
        #             item['parking'],
        #             pymysql.escape_string(item['lot']),
        #
        #         )
        #     )
        #     tit = self.cursor.lastrowid
        # self.conn.commit()
        return item
