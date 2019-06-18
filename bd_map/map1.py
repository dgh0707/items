# -*- coding: utf-8 -*-

# 获取百度地图ak值的链接：http://lbsyun.baidu.com/apiconsole/key
# 服务文档链接：http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-placeapi
from urllib import request
import map2
from bs4 import BeautifulSoup
import json
'''r=request.urlopen('http://api.map.baidu.com/place/v2/search?query=学校&region=南京市建邺区&output=json&ak=LzFMkD5cuezTba5nXv6gKtjNcvqY7fMe')
#将数据反序列化到内存
html=json.loads(r.read().decode("utf8"))
results=html['results']
print(results)
for i in results:
    #酒店名字
    name=i['name']
    #地址
    # address=i['address']
    #经纬度
    location=i['location']
    #电话
    try:
        telephone=i['telephone']
    except:
        pass
    # print(name,address,location,telephone)

    # #酒店价格
    # try:
    #     price=i['detail_info']['price']
    # except:
    #     pass
    # #酒店详细信息URL
    # detail_url=i['detail_info']['detail_url']
    print(location)

    # print(price,detail_url)
    # map2.save(name, address, location, telephone, price, detail_url)'''



import requests
list=['上海']

w = '宠物店'

for j in list:
    url = 'http://api.map.baidu.com/place/v2/search?query='+str(w)+'&region='+str(j)+'&page_size=10&page_num=0&output=json&ak=LzFMkD5cuezTba5nXv6gKtjNcvqY7fMe'
    # uid= 'd305db1f9f2e0827932ca3c2'
    # url = 'http://api.map.baidu.com/place/v2/detail?uid='+str(uid)+'8&output=json&scope=2&ak=LzFMkD5cuezTba5nXv6gKtjNcvqY7fMe'
    res = requests.get(url).text
    print(res)
    print(url)
    # res = json.loads(res)
    # results = res['results']
    # for i in results:
    #     try:
    #         name = i['name']
    #         location = i['location']
    #         lat = location['lat']
    #         lng = location['lng']
    #         location = str(lat)+','+str(lng)
    #         print(name,location)
    #         map2.save(name,location)
    #     except:
    #         pass
