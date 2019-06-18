# -*- coding: utf-8 -*-
import os
import re
import time

import scrapy
import json
from yunji.items import YunjiItem
from urllib import request
import requests


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['https://vipapp.yunjiglobal.com']
    # start_urls = ['http://https://vipapp.yunjiglobal.com/']

    def start_requests(self):
        start_urls = 'https://vipapp.yunjiglobal.com/yunjiapp4buyer/app4buyer/item/listSubCategoryByParentId.json?parentCategoryId=90'
        yield scrapy.Request(start_urls,callback=self.get_category,dont_filter=True)

    # 获取子模块的分类ID和分类名
    def get_category(self,response):
        res = response.text
        category_list = json.loads(res)['data']
        for category in category_list:
            categoryLevelId = category['categoryLevelId']
            for i in range(29,30):
                url = 'https://vipapp.yunjiglobal.com/yunjiapp4buyer/app4buyer/item/getListItemByCategoryIdV1.json?pageIndex='+str(i)+'&pageSize=10&categoryLevelId1=90&categoryLevelId2='+str(categoryLevelId)
                categoryLevelName = category['categoryLevelName']
                yield scrapy.Request(url,meta={'categoryLevelName':categoryLevelName},callback=self.parse,dont_filter=True)
                time.sleep(0.5)

    def parse(self, response):

        item = YunjiItem()
        res = response.text
        js_list = json.loads(res)['data']

        for js in js_list:
            # 父类模块分类
            item['parent_category'] = '服饰箱包'
            # 子类模块分类
            item['category'] = response.meta['categoryLevelName']
            # 商品id
            item['aid'] = str(js['itemId'])
            # 名称
            item['title'] = js['itemName']
            # 销售价格
            item['price'] = js['itemPrice']
            # 原价
            item['vprice'] = js['itemVipPrice']
            # 品牌
            item['brand'] = js['itemBrandName']
        # 商品主图的url地址
            img_list = js['bigImgList']
            oss_imgpath_list=[]
            # 商品主图下载
            try:
                os.mkdir('E:/商城图片/云集APP/img/' + str(item['aid']))
            except:
                pass
            for j in img_list:
                request.urlretrieve(j, 'E:/商城图片/云集APP/img/' + str(item['aid']) + '/' + j.split('/')[-1])
                time.sleep(0.5)
                print('-------正在下载%s主图图片---------' % item['aid'])

                img_url = j.split('/')[-1]
                oss_path = 'https://redbag-imgs.oss-cn-beijing.aliyuncs.com/mall/2019/yunji/img/'+item['aid']+'/'+img_url
                oss_imgpath_list.append(oss_path)
            item['oss_imgpath_list'] = oss_imgpath_list

        # 请求解析详情图的url链接
            image_url = 'https://item.yunjiglobal.com/yunjiitemapp/buyer/item/getItemDetailInfo.json?itemId='+item['aid']
            res = requests.get(image_url,verify=False).text
            time.sleep(0.5)

            data = json.loads(res)['data']

        # 商品参数图片上传OSS的url
            if 'itemParameters' in res:
                if re.findall('img title=\"(.*?)"', data['itemParameters']):
                    global Parameters
                    Parameters = ''.join(re.findall('img title=\"(.*?)"', data['itemParameters']))
                elif re.findall('img src=\"(.*?)"', data['itemParameters']):
                    Parameters = ''.join(re.findall('img src=\"(.*?)"', data['itemParameters']))
            # 参数图片下载
                try:
                    os.mkdir('E:/商城图片/云集APP/parmeter/' + str(item['aid']))
                except:
                    pass
                request.urlretrieve(Parameters,'E:/商城图片/云集APP/parmeter/' + str(item['aid']) + '/' + Parameters.split('/')[-1])
                print('-------正在下载参数图片%s---------' % item['aid'])

                Parameters = Parameters.split('/')[-1]
                item['oss_parameters'] = 'https://redbag-imgs.oss-cn-beijing.aliyuncs.com/mall/2019/yunji/parameter/'+item['aid']+'/'+str(Parameters)
                item['parameters'] =''
            elif 'spuProperty' in res:
                Parameters = data['spuProperty']
                item['parameters'] = Parameters
                item['oss_parameters'] = ''

        # 商品详情图地址
            js_list = json.loads(res)['data']['itemDetail']
            if re.findall('img src="(.*?)"', js_list):
                image_list = re.findall('img src="(.*?)"', js_list)
            elif re.findall('img title="(.*?)"', js_list):
                image_list = re.findall('img title="(.*?)"', js_list)

            try:
                os.mkdir('E:/商城图片/云集APP/image/' + str(item['aid']))
            except:
                pass

            oss_imagepath_list = []
            i = 0
            for image in image_list:
                image_id = i + 1
                i = image_id
                request.urlretrieve(image, 'E:/商城图片/云集APP/image/' + str(item['aid']) + '/' + str(image_id) + '.jpg')
                time.sleep(0.5)
                print('-------正在下载详情图片%d---------' % image_id)

                oss_path = 'https://redbag-imgs.oss-cn-beijing.aliyuncs.com/mall/2019/yunji/image/'+item['aid']+'/'+str(image_id)+'.jpg'
                oss_imagepath_list.append(oss_path)
            item['oss_imagepath_list'] = oss_imagepath_list


            yield item
            time.sleep(0.5)



