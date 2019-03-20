'''
有声小说的网站数据
爬虫+语音识别+web网站、

'''

import requests,os
from lxml import etree

class Sprder(object):

    def start_res(self):
        response=requests.get("https://www.qidian.com/all")
        html=etree.HTML(response.content.decode())
        # print(html)
        title_list = html.xpath('//div[@class="book-mid-info"]/h4/a/text()')
        src_list = html.xpath('//div[@class="book-mid-info"]/h4/a/@href')
        # print(title_list, src_list)
        for title,src in zip(title_list,src_list):
            if os.path.exists(title)== False:
                os.mkdir(title)
            self.file_data(title,src)

    def file_data(self,title,src):

        res = requests.get('https:'+src)
        html = etree.HTML(res.content.decode())
        tit_list = html.xpath('//ul[@class="cf"]/li/a/text()')
        sr_list = html.xpath('//ul[@class="cf"]/li/a/@href')
        for tit,sr in zip(tit_list,sr_list) :
            self.save_data(tit,sr,title)
            # print(title,tit,sr)

    def save_data(self,tit,sr,title):
        res = requests.get('https:'+sr)
        html = etree.HTML(res.content.decode())
        content = '\n'.join(html.xpath('//div[@class="read-content j_readContent"]/p/text()'))
        file_name = title + '\\' + tit
        print('正在爬取文章：',file_name)
        with open(file_name+".txt",'a',encoding='utf8')as f:
            f.write(content)


sprder=Sprder()
sprder.start_res()