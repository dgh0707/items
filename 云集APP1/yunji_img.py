#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
@File    : yunji_img.py
@software: PyCharm
@Time    : 2019/6/10 10:24

'''
import os
import time

'''
SSL证书的验证链接：https://2.python-requests.org//zh_CN/latest/user/advanced.html#ssl

'''

from urllib import request
import requests
import json,re
import pymysql
import pandas as pd



class Spider():
    def __init__(self):
        pass

    def get_parse(self,url,aid):
        res = requests.get(url,verify=False).text
        js_list = json.loads(res)['data']

        itemid = aid
        img_list = js_list['bigImgList']
        print(itemid)
        # 商品主图下载
        try:
            os.mkdir('E:/商城图片/云集APP1/img/' + str(itemid))
        except:
            pass
        for img in img_list:
            request.urlretrieve(img,'E:/商城图片/云集APP1/img/' + str(itemid) + '/' + img.split('/')[-1])
            time.sleep(0.5)
            print('-------正在下载%s主图图片---------' % itemid)

        self.dow_img(itemid)
        time.sleep(0.5)
    def dow_img(self,itemid):
        url = 'https://item.yunjiglobal.com/yunjiitemapp/buyer/item/getItemDetailInfo.json?itemId='+str(itemid)
        res = requests.get(url, verify=False).text
        data = json.loads(res)['data']
    # 商品参数图片下载
        if 'itemParameters' in res:
            if re.findall('img title=\"(.*?)"', data['itemParameters']):
                global Parameters
                Parameters = re.findall('img title=\"(.*?)"', data['itemParameters'])
            elif re.findall('img src=\"(.*?)"', data['itemParameters']):
                Parameters = re.findall('img src=\"(.*?)"', data['itemParameters'])
            # 参数图片下载
            try:
                os.mkdir(r'E:/商城图片/云集APP1/parameter/' + str(itemid))
            except:
                pass
            for i in Parameters:
                Parameters = i
                request.urlretrieve(Parameters,'E:/商城图片/云集APP1/parameter/' + str(itemid) + '/' + Parameters.split('/')[-1])
                print('-------正在下载参数图片%s---------' % str(itemid))
    # 商品详情图下载
        js_list = json.loads(res)['data']['itemDetail']
        if re.findall('img src="(.*?)"', js_list):
            image_list = re.findall('img src="(.*?)"', js_list)
        elif re.findall('img title="(.*?)"', js_list):
            image_list = re.findall('img title="(.*?)"', js_list)
        try:
            os.mkdir('E:/商城图片/云集APP1/image/' + str(itemid))
        except:
            pass
        i = 0
        for image in image_list:
            image_id = i + 1
            i = image_id
            request.urlretrieve(image, 'E:/商城图片/云集APP1/image/' + str(itemid) + '/' + str(image_id) + '.jpg')
            time.sleep(0.5)
            print('-------正在下载详情图片%d---------' % image_id)



if __name__ == '__main__':
    # 连接数据库
    conn = pymysql.connect(user='share_hunter', passwd='2018@Amber123', db='apst_share', host='47.93.244.121',
                           charset='utf8')
    cursor = conn.cursor()
    list_id = cursor.execute("select aid from yunji where img_status = 0 and parent_category = '美妆个护'")
    # list_id = cursor.execute("select aid from yunji where aid = '152839'")
    df = cursor.fetchmany(list_id)[180:200]
    for aid in df:
        aid = aid[0]

        # aid = '1076'
        url ='https://vipapp.yunjiglobal.com/yunjiapp4buyer/app4buyer/item/getItemBoV1.json?itemId='+str(aid)
        headers = {
            'User-Agent': 'okhttp/3.6.0',
            'Cookie': 'aliyungf_tc=AQAAAE8+/nBJLwIAHgto3/J73pYI7oOg',

        }
        s = Spider()
        s.get_parse(url,aid)
    cursor.close()
    conn.close()

