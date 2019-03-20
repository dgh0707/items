#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
@File    : upload_img.py
@software: PyCharm
@Time    : 2019/3/11 16:05

'''

import oss2
import os
import pymysql

# 将本地的图片上传到OSS
access_key_id= 'LTAI8xfaawqULMb9'
access_key_secret = '7TTsDBGY65MRyxjVdUQNECSN9r7TtE'
endpoint = 'oss-cn-beijing.aliyuncs.com'
endpoint_internal = 'oss-cn-beijing-internal.aliyuncs.com'
bucket_name = 'redbag-imgs'

ossdir = 'mall/2019/jingdong/image/'
# ossdir = 'mall/2019/jingdong/img/'


auth = oss2.Auth(access_key_id,access_key_secret)
bucket = oss2.Bucket(auth,endpoint,bucket_name)

def uploadFile(file):
    remoteName = ossdir+file.replace(basedir, '').replace('\\','/')[1:]

    date_file = remoteName.split('/')[4]
    print(remoteName, file)
    bucket.put_object_from_file(remoteName, file)
    print('---------正在上传图片：%s----------'% date_file)

    # 数据库连接,改变状态值
    conn = pymysql.connect(user='root', passwd='123456', db='taobao',
                                    host='localhost', charset='utf8')
    cursor = conn.cursor()
    # 主图上传的状态(limit 1表示只修改1条)
    # cursor.execute("update jd set img_status=1 where cid=" + date_file + " limit 1")

    # 详情图片的状态
    cursor.execute("update jd set image_status=1 where cid=" + date_file + " limit 1")
    conn.commit()

    # print('========%s 图片上传成功========'% date_file)

def list(dir):# 判断文件夹下一层是否还存在文件就夹，是的话继续遍历，否则执行uploadFile(file)
    fs = os.listdir(dir)
    for f in fs:
        file = dir + "\\" + f
        if os.path.isdir(file):
            list(file)
        else:
            uploadFile(file)

basedir = r'D:\amber\ITEMS\京东\jingdong\image'
# basedir = r'D:\amber\ITEMS\京东\jingdong\img'

list(basedir)
