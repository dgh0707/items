# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql

class JingdongPipeline(object):
    def __init__(self):
        # self.conn = pymysql.connect(user='root', passwd='123456', db='taobao',
        #                             host='localhost', charset='utf8')
        # self.cursor = self.conn.cursor()
        # self.cursor.execute('truncate qw_goods;')
        # self.conn.commit()

        self.conn = pymysql.connect(user='root', passwd='2018@Amber123', db='apst_share',
                                    host='47.93.244.121', charset='utf8')
        self.cursor = self.conn.cursor()
        # self.cursor.execute('truncate qw_goods;')
        # self.conn.commit()

    def process_item(self, item, spider):
        # tit = self.cursor.execute('select id from jd where cid=%s', (item['cid']))
        # if tit:
        #     tit = self.cursor.fetchone()
        # else:
        #     self.cursor.execute(
        #         """INSERT INTO jd (cid,goods_number,title,auctionUrl,price,brand,comm_attr,oss_imgurl,oss_imageurl)VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s")""" %
        #         (
        #             item['cid'],
        #             item['comm_id'],
        #             item['title'],
        #             item['auctionUrl'],
        #             pymysql.escape_string(item['price']),
        #             item['brand'],
        #             pymysql.escape_string(item['comm_attr']),
        #             pymysql.escape_string(item['oss_imgurl']),
        #             pymysql.escape_string(item['oss_imageurl']),
        #
        #         )
        #     )
        #     tit = self.cursor.lastrowid
        # self.conn.commit()
        tit = self.cursor.execute('select id from qw_goods where goods_number=%s', (item['comm_id']))
        if tit:

            tit = self.cursor.fetchone()
        else:
            self.cursor.execute(
                """INSERT INTO qw_goods (cid,goods_number,brand,goodsname,auctionurl,goodsprice,goods_attribute,goodsthumb,details,discount_price)VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")""" %
                (
                    item['cid'],
                    item['comm_id'],
                    pymysql.escape_string(item['brand']),
                    item['title'],
                    item['auctionUrl'],
                    item['price'],
                    pymysql.escape_string(item['comm_attr']),
                    pymysql.escape_string(item['oss_imgurl']),
                    pymysql.escape_string(item['oss_imageurl']),
                    item['discount_price'],

                )
            )
            tit = self.cursor.lastrowid

        self.conn.commit()
        return item
