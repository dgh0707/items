# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

class YelpPipeline(object):
    def __init__(self):
    #     # self.conn = pymysql.connect(user='root', passwd='123456', db='zhizihua',
    #     #                             host='localhost', charset='utf8')
    #     # self.cursor = self.conn.cursor()
    #     # # self.cursor.execute('truncate yelp;')
    #     # # self.conn.commit()
    #
    #     # 测试数据库
          self.conn = pymysql.connect(user='root', passwd='2018@Amber123', db='apst_share',
                                        host='47.93.244.121', charset='utf8')
          self.cursor = self.conn.cursor()
        
    def process_item(self, item, spider):
        tit = self.cursor.execute('select id from yelp where detail_page_url=%s', (item['detail_page_url']))
        if tit:

            tit = self.cursor.fetchone()
        else:
            self.cursor.execute(
                """INSERT INTO yelp (detail_page_url,city,`name`,street,address,tel,forms,email,logo_imgurl,back_img,latitude,longitude,description)VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")""" %
                (
                    item['detail_page_url'],
                    item['city'],
                    item['name'],
                    item['street'],
                    pymysql.escape_string(item['address']),
                    item['tel'],
                    item['forms'],
                    pymysql.escape_string(item['email']),
                    item['logo_imgurl'],
                    item['back_img'],
                    item['latitude'],
                    item['longitude'],
                    pymysql.escape_string(item['description']),

                )
            )
            tit = self.cursor.lastrowid
        self.conn.commit()
        return item
