#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
@File    : yelp.py
@software: PyCharm
@Time    : 2019/5/14 14:10

'''
import random
import re
import time

import requests
from lxml import etree

url = 'https://www.yelp.com/biz/bulkin-building-san-francisco'
header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',

    }
res = requests.get(url,headers=header).text

html = etree.HTML(res)
#                           //*[@id="wrap"]/div[2]/div/div[1]/div/div[3]/div[1]/div[2]/div/span/a[1]
forms = ''.join(html.xpath('//div[@class="biz-main-info embossed-text-white"]/div/span/text()'))
print(forms)
# if html.xpath('//*[@id="wrap"]/div[2]/div/div[1]/div/div[4]/div[1]/div/div[2]/ul/li[1]/div/address'):
#     address = ''.join(html.xpath('//*[@id="wrap"]/div[2]/div/div[1]/div/div[4]/div[1]/div/div[2]/ul/li[1]/div/address/text()')).strip().replace("\n", "")
# elif html.xpath('//*[@id="wrap"]/div[2]/div/div[1]/div/div[4]/div[1]/div/div[2]/ul/li[1]/div/strong'):
#     address = ''.join(html.xpath('//*[@id="wrap"]/div[2]/div/div[1]/div/div[4]/div[1]/div/div[2]/ul/li[1]/div/strong/address/text()')).strip().replace("\n", "")
# address = ''.join(html.xpath('//*[@id="wrap"]/div[2]/div/div[1]/div/div[4]/div[1]/div/div[2]/ul/li[1]/div/address/text()')).strip().replace("\n", "").replace(" ", "")
# print(address)
# 73SumnerStUnit205SanFrancisco,CA94103
# address = '73SumnerStUnit205SanFrancisco,CA94103'
# l= list(address)
# for i in l:
#     if i.isupper():
#         index = l.index(i)
#         l.insert(index,' ')
# print(l)







'''class Spider():
    def __init__(self):
        pass

    def start_res(self,url,header,proxy):
        res = requests.get(url,headers=header,proxies=proxy).text
        html = etree.HTML(res)
        aurl_list = html.xpath('//*[@id="wrap"]/div[3]/div[2]/div[2]/div/div[1]/div[1]/div/ul/li/div/div/div[1]/div[2]/div/div[1]/div[1]/div[1]/h3/a/@href')
        forms_list = html.xpath('//*[@id="wrap"]/div[3]/div[2]/div[2]/div/div[1]/div[1]/div/ul/li/div/div/div[1]/div[2]/div/div[1]/div[1]/div[4]/span/span/span/a/text()')
        print(len(aurl_list))
        for url1,forms in zip(aurl_list,forms_list):
            if '/adredir?' in url1 :
                url_meta = ''.join(re.findall('com%2Fbiz%2F(.*?)&request_id',url1))
                aurl = 'https://www.yelp.com/biz/'+ str(url_meta)
            else:
                aurl = 'https://www.yelp.com'+url1
            forms = forms
            print(aurl)
            self.get_data(aurl,forms,header)
    def get_data(self,aurl,forms,header):
        res = requests.get(aurl,headers=header).text
        html = etree.HTML(res)
        time.sleep(0.5)

        item = {'parent_level':'','name':'','forms':''}
        # 父类标签
        item['parent_level'] = 'Contractors'
        # 名称                      //*[@id="wrap"]/div[2]/div/div[1]/div/div[3]/div[1]/div[1]/h1
        name1 = ''.join(html.xpath('//div[@class="biz-page-header-left claim-status"]/div/h1/text()'))
        name2 = ''.join(html.xpath('//div[@class="biz-page-header-left claim-status"]/div/div/h1/text()'))
        item['name'] = name1 + name2

        # 类别
        item['forms'] = forms

        print(item)



if __name__ == '__main__':
    s = Spider()
    url = 'https://www.yelp.com/search?cflt=contractors&find_loc=San%20Francisco%2C%20CA%2C%20US&start=0'
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',

    }
    proxy = {
        "http": "http://149.129.101.202:8080",
        "https": "https://149.129.101.202:8080",

    }

    s.start_res(url,header,proxy)'''





