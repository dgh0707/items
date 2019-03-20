# -*- coding: utf-8 -*-
import scrapy
from jingdong.items import JingdongItem
import time
import json,os,re
from urllib import request
import requests


class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']
    keyword = '美妆'
    n = 92
    page = 2*n-1
    url = 'https://search.jd.com/Search?keyword=%s&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%s&suggest=1.his.0.0&stock=1&page=%d'
    next_url = 'https://search.jd.com/s_new.php?keyword=%s&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%s&stock=1&page=%d&scrolling=y&tpl=1_M&show_items=%s'

    @staticmethod
    def _clean_str(items):
        for key in items:
            if items[key]:
                items[key] = items[key].strip().replace("\n", "").replace("", "").replace("", "")
                if items[key] == '':
                    items[key] = None

        return items
    def start_requests(self):

        yield scrapy.Request(url=self.url%(self.keyword,self.keyword,self.page), callback=self.parse, dont_filter=True)


    def parse(self, response):

        id_list = response.xpath('//ul[@class="gl-warp clearfix"]/li/@data-sku').extract()
        price_list = response.xpath('//ul[@class="gl-warp clearfix"]/li/div/div[2]/strong/i/text()').extract()

        for auctionUrl,price in zip(id_list,price_list):
            auctionUrl ='https://item.jd.com/'+str(auctionUrl)+'.html'
            price = price
            yield scrapy.Request(auctionUrl,callback=self.info_parse,meta={'auctionUrl':auctionUrl,'price':price})
        time.sleep(1)

    # 获取每页的后30条列表的数据
        headers = {'referer': response.url}
        self.page += 1
        yield scrapy.Request(self.next_url % (self.keyword, self.keyword,self.page, ','.join(id_list)),
                             callback=self.next_parse, headers=headers)
        time.sleep(1)

    def next_parse(self,response):
        id_list = response.xpath('//li[@class="gl-item"]/@data-sku').extract()
        price_list = response.xpath('//li[@class="gl-item"]/div/div[2]/strong/i/text()').extract()
        for auctionUrl,price in zip(id_list,price_list):
            auctionUrl ='https://item.jd.com/'+str(auctionUrl)+'.html'
            price = price
            yield scrapy.Request(auctionUrl,callback=self.info_parse,meta={'auctionUrl':auctionUrl,'price':price})

        # if 1 <= self.n < 3:
        #     self.n += 1
        #     self.page = 2 * self.n - 1
        #     yield scrapy.Request(self.url%(self.keyword,self.page), callback=self.parse, dont_filter=True)


    def info_parse(self,response):
        # res = response.text
        item = JingdongItem()
        # 商品类型  美妆：1
        item['cid'] = '1'
        # 商品的ID
        item['comm_id'] = response.meta['auctionUrl'].split('/')[-1].split('.')[0]
        # 商品的名称
        title = response.xpath('//div[@class="sku-name"]/text()').extract()

        item['title'] = ''.join(title)
        # if response.xpath('//div[@class="sku-name"]/text()'):
        #     item['title'] = response.xpath('//div[@class="sku-name"]/text()').extract_first()
        # elif response.xpath('//div[@class="sku-name"]/img/text()'):
        #     item['title'] = response.xpath('//div[@class="sku-name"]/img/text()').extract_first()
        # 商品的详情页的URL地址
        item['auctionUrl'] = response.meta['auctionUrl']
        # 商品的价格
        item['price'] = response.meta['price']
        # 折扣价
        item['discount_price'] = response.meta['price']
        # 商品的品牌
        brand_dict = {"brand": "", "status": 0}
        item['brand'] = ''.join(response.xpath('//ul[@id="parameter-brand"]/li/a/text()').extract())
        # brand_dict['brand'] = brand
        # item['brand'] = json.dumps(brand_dict, ensure_ascii=False)
        # 商品的参数属性
        if response.xpath('//ul[@class="parameter2 p-parameter-list"]/li/text()').extract():
            comm_attr = response.xpath('//ul[@class="parameter2 p-parameter-list"]/li/text()').extract()
            item['comm_attr'] = json.dumps(comm_attr, ensure_ascii=False)
        elif response.xpath('//ul[@class="parameter2"]/li/text()').extract():
            comm_attr = response.xpath('//ul[@class="parameter2"]/li/text()').extract()
            item['comm_attr'] = json.dumps(comm_attr, ensure_ascii=False)

    # 图片下载
    #   商品的主图URL地址
        img_url_list = response.xpath('//ul[@class="lh"]/li/img/@data-url').extract()
        try:
            os.mkdir('img/' + item['comm_id'])
        except:
            pass
        oss_imgurl_list = []
        i = 0
        for img_url in img_url_list:
            img_url = 'http://img11.360buyimg.com/n1/' + img_url
            request.urlretrieve(img_url, 'img/' + item['comm_id'] + '/' + img_url.split('/')[-1])
            time.sleep(0.5)
            print('-------正在下载%s主图图片---------'%item['comm_id'])
        # 拼接OSS的图片地址
            img_dict = {"id": '', "imgurl": "", "status": 0, "describe": ""}
            oss_url = 'https://redbag-imgs.oss-cn-beijing.aliyuncs.com/mall/2019/jingdong/img/' + item['comm_id'] + '/' + img_url.split('/')[-1] + '?x-oss-process=image/quality,q_60'
            img_dict['imgurl'] = oss_url
            img_dict['id'] = i + 1
            i = img_dict['id']
            oss_imgurl_list.append(img_dict)
        item['oss_imgurl'] = json.dumps(oss_imgurl_list, ensure_ascii=False)
        # item['oss_imgurl'] = ''
        time.sleep(0.5)

        # 商品详情图
        if re.findall('mainSkuId=(\d+)',response.text):
            mainSkuId = ''.join(re.findall('mainSkuId=(\d+)',response.text))
        elif re.findall("mainSkuId:'(\d+)'",response.text):
            mainSkuId = ''.join(re.findall("mainSkuId:'(\d+)'", response.text))
        else:
            mainSkuId = item['cid']
        image_url = 'https://cd.jd.com/description/channel?skuId=' + item['comm_id'] + '&mainSkuId=' + str(mainSkuId)
        res = requests.get(image_url).text
        res = json.loads(res)
        content = res['content']
        if re.findall('url\((.*?)\);', content):
            image_url_list = re.findall('url\((.*?)\);', content)
        elif re.findall('data-lazyload=\"(.*?)\"', content):
            image_url_list = re.findall('data-lazyload=\"(.*?)\"', content)
        elif re.findall("data-lazyload='(.*?)'", content):
            image_url_list = re.findall("data-lazyload='(.*?)'", content)
        try:
            os.mkdir('image/' + item['comm_id'])
        except:
            pass
        oss_imageurl_list = []
        i = 0
        for image_url in image_url_list:

            image_id = i + 1
            i = image_id
            if "http" in image_url:
                image_url = image_url
            else:
                image_url = 'https:' + image_url
            request.urlretrieve(image_url, 'image/' + item['comm_id'] + '/' + str(image_id)+'.jpg')
            time.sleep(0.5)
            print('-------正在下载详情图片%d---------'%image_id)
        # 拼接详情图的OSS地址
            image_dict = {"id": '', "imageurl": "", "status": 0, "describe": ""}
            oss_url = 'https://redbag-imgs.oss-cn-beijing.aliyuncs.com/mall/2019/jingdong/image/' + item['comm_id'] + '/' + str(image_id) + '.jpg?x-oss-process=image/quality,q_60'
            image_dict['imageurl'] = oss_url
            image_dict['id'] = str(image_id)

            oss_imageurl_list.append(image_dict)
        item['oss_imageurl'] = json.dumps(oss_imageurl_list, ensure_ascii=False)
        # item['oss_imageurl'] =''
        time.sleep(0.5)

        yield self._clean_str(item)
        time.sleep(0.5)





