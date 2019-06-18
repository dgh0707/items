# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql

class YunjiPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(user='root', passwd='2018@Amber123', db='apst_share',
                                    host='47.93.244.121', charset='utf8')
        self.cursor = self.conn.cursor()

        # self.cursor.execute('truncate yunji;')
        # self.conn.commit()

    def process_item(self, item, spider):
        self.conn.ping(reconnect=True)
        tit = self.cursor.execute('select id from yunji where aid=%s', (item['aid']))
        if tit:

            tit = self.cursor.fetchone()
        else:
            self.cursor.execute(
                """INSERT INTO yunji (parent_category,category,aid,title,price,vprice,brand,oss_imgpath_list,oss_imagepath_list,oss_parameters,parameters)VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")""" %
                (
                    item['parent_category'],
                    item['category'],
                    item['aid'],
                    item['title'],
                    item['price'],
                    item['vprice'],
                    item['brand'],
                    item['oss_imgpath_list'],
                    item['oss_imagepath_list'],
                    item['oss_parameters'],
                    item['parameters'],

                )
            )
            tit = self.cursor.lastrowid

        self.conn.commit()



        return item
