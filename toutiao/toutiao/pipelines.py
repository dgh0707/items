# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

class ToutiaoPipeline(object):
    # def __init__(self):
    #     self.conn = pymysql.connect(user='root', passwd='123456', db='caijing',
    #                                 host='localhost', charset='utf8')
    #     self.cursor = self.conn.cursor()
    #     self.cursor.execute('truncate cj;')
    #     self.conn.commit()
    def __init__(self):
        self.conn = pymysql.connect(user='news_user', passwd='Amber123', db='capital_future',
                                    host='java-dev.4summer.cn', charset='utf8')
        self.cursor = self.conn.cursor()


    def process_item(self, item, spider):
        tit = self.cursor.execute('select id from pre_news_models where article_id=%s', (item['article_id']))
        if tit:
            tit = self.cursor.fetchone()
        else:
            self.cursor.execute(
                """INSERT INTO pre_news_models (title,writer,publish_time,read_number,summary,article,tags,class_id,article_id,image)VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")""" %
                (
                    item['title'],
                    item['writer'],
                    item['publish_time'],
                    item['read_number'],
                    item['summary'],
                    pymysql.escape_string(item['article']),
                    item['tags'],
                    pymysql.escape_string(item['class_id']),
                    item['article_id'],
                    item['oss_url1'],
                )
            )
            tit = self.cursor.lastrowid

        self.cursor.execute("update pre_news_models set status=1 where image='https://capital-future-imgs.oss-cn-beijing.aliyuncs.com/images/new_default.png?x-oss-process=image/resize,l_500'")

        self.conn.commit()
        return item
