# -*- coding: utf-8 -*-
from pymysql import *
# def save(*args):
#     conn = connect(host='localhost', port=3306,user='root',passwd='123456',db='map1',charset='utf8')
#     cursor=conn.cursor()
#     query = cursor.execute('INSERT INTO sj(`name`,`address`,`location`,`telephone`,`price`,`detail_url`)VALUES("%s", "%s", "%s", "%s", "%s", "%s")' % (args[0], args[1], args[2], args[3], args[4], args[5]))
#
#     conn.commit()
#     cursor.close()
#     conn.close()

def save(*args):
    conn = connect(host='localhost', port=3306,user='root',passwd='123456',db='taobao',charset='utf8')
    cursor=conn.cursor()
    query = cursor.execute('INSERT INTO xx(`name`,`location`)VALUES("%s", "%s")' % (args[0], args[1]))

    conn.commit()
    cursor.close()
    conn.close()