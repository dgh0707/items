# -*- coding: utf-8 -*-
import os
import re
import time

import scrapy
from yelp.items import YelpItem
from urllib import request


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['www.yelp.com']
    # start_urls = ['http://https://www.yelp.com//']

    def start_requests(self):
        # 一共90页的数据
        for i in range(96,100):
        # i= 55[contractors,electricians]
            start_urls = 'https://www.yelp.com/search?cflt=electricians&find_loc=Oakland%2C%20CA&start='+ str(i*10)
            yield scrapy.Request(url=start_urls, callback=self.parse, dont_filter=True)
            time.sleep(0.5)

    @staticmethod
    def _clean_str(item):
        for key in item:
            if item[key]:
                item[key] = item[key].strip().replace("\n", "").replace(" ", "")
                if item[key] == '':
                    item[key] = None
    def parse(self, response):
        # 详情页面的URL地址列表
        aurl_list = response.xpath('//*[@id="wrap"]/div[3]/div[2]/div[2]/div/div[1]/div[1]/div/ul/li/div/div/div[1]/div[2]/div/div[1]/div[1]/div[1]/h3/a/@href').extract()
        # 分类列表
        forms_list = ''.join(response.xpath('//*[@id="wrap"]/div[3]/div[2]/div[2]/div/div[1]/div[1]/div/ul/li/div/div/div[1]/div[2]/div/div[1]/div[1]/div[4]/span/span/span/a/text()').extract())
        # 列表页logo图
        if response.xpath('//*[@id="wrap"]/div[3]/div[2]/div[2]/div/div[1]/div[1]/div/ul/li/div/div/div[1]/div[1]/div/div/a/img/@src'):
            logo_imgurl_list = response.xpath('//*[@id="wrap"]/div[3]/div[2]/div[2]/div/div[1]/div[1]/div/ul/li/div/div/div[1]/div[1]/div/div/a/img/@src').extract()
        elif response.xpath('//*[@id="wrap"]/div[3]/div[2]/div[2]/div/div[1]/div[1]/div/ul/li/div/div/div/div[1]/div/div/div/div/div/a/img/@src'):
            logo_imgurl_list = response.xpath('//*[@id="wrap"]/div[3]/div[2]/div[2]/div/div[1]/div[1]/div/ul/li/div/div/div/div[1]/div/div/div/div/div/a/img/@src').extract()
        for url1,logo_imgurl in zip(aurl_list,logo_imgurl_list):
            if '/adredir?' in url1 :
                url_meta = ''.join(re.findall('com%2Fbiz%2F(.*?)&request_id',url1))
                aurl = 'https://www.yelp.com/biz/'+ str(url_meta)
            else:
                aurl = 'https://www.yelp.com'+url1

            yield scrapy.Request(url=aurl, callback=self.parse1, meta={'forms':forms_list,'logo_imgurl':logo_imgurl,'aurl':aurl},dont_filter=True)
            time.sleep(0.5)

    def parse1(self,response):
        item = YelpItem()
        # 详情页面URL
        item['detail_page_url'] = response.meta['aurl']
        # 城市
        item['city'] = 'Oakland, CA'
        # 名称
        name1 = ''.join(response.xpath('//div[@class="biz-page-header-left claim-status"]/div/h1/text()').extract())
        name2 = ''.join(response.xpath('//div[@class="biz-page-header-left claim-status"]/div/div/h1/text()').extract())
        item['name'] = name1 + name2

        # 电话
        if response.xpath('//div[@class="mapbox-text"]/ul/li[2]/span[3]/text()'):
            item['tel'] = ''.join(response.xpath('//div[@class="mapbox-text"]/ul/li[2]/span[3]/text()').extract()).replace("\n", "").replace(" ", "")
        elif response.xpath('//div[@class="mapbox-text"]/ul/li[3]/span[3]/text()'):
            item['tel'] = ''.join(response.xpath('//div[@class="mapbox-text"]/ul/li[3]/span[3]/text()').extract()).replace("\n", "").replace(" ", "")
        else:
            item['tel'] = ''


        # 街道
        item['street'] =''.join(response.xpath('//*[@id="wrap"]/div[2]/div/div[1]/div/div[4]/div[1]/div/div[2]/ul/li[1]/div/strong/text()').extract()).strip().replace("\n", "")

        # 地址
        if response.xpath('//*[@id="wrap"]/div[2]/div/div[1]/div/div[4]/div[1]/div/div[2]/ul/li[1]/div/address'):
            item['address'] =  ''.join(response.xpath('//*[@id="wrap"]/div[2]/div/div[1]/div/div[4]/div[1]/div/div[2]/ul/li[1]/div/address/text()').extract()).strip().replace("\n", "")
        elif response.xpath('//*[@id="wrap"]/div[2]/div/div[1]/div/div[4]/div[1]/div/div[2]/ul/li[1]/div/strong'):
            item['address'] = ''.join(response.xpath('//*[@id="wrap"]/div[2]/div/div[1]/div/div[4]/div[1]/div/div[2]/ul/li[1]/div/strong/address/text()').extract()).strip().replace("\n", "")
        else:
            item['address'] = ''


        # 官网
        if response.xpath('//*[@id="wrap"]/div[2]/div/div[1]/div/div[4]/div[1]/div/div[2]/ul/li[3]/span[2]/a/@href'):
            email = ''.join(response.xpath('//*[@id="wrap"]/div[2]/div/div[1]/div/div[4]/div[1]/div/div[2]/ul/li[3]/span[2]/a/@href').extract())
            email = email.split('&website_link')[0].split('2F')[-1]
            item['email'] = email
        elif response.xpath('//*[@id="wrap"]/div[2]/div/div[1]/div/div[4]/div[1]/div/div[2]/ul/li[4]/span[2]/a/@href'):
            email = ''.join(response.xpath('//*[@id="wrap"]/div[2]/div/div[1]/div/div[4]/div[1]/div/div[2]/ul/li[4]/span[2]/a/@href').extract())
            email = email.split('&website_link')[0].split('2F')[-1]
            item['email'] =  email
        else:
            item['email'] = ''

        # 分类
        if response.xpath('//div[@class="biz-main-info embossed-text-white"]/div[2]/span[2]/a/text()'):
            item['forms'] = ''.join(response.xpath('//div[@class="biz-main-info embossed-text-white"]/div[2]/span[2]').xpath('string(.)').extract()).replace("\n", "").replace(" ", "")
        elif response.xpath('//div[@class="biz-main-info embossed-text-white"]/div[2]/span/a/text()'):
            item['forms'] = ''.join(response.xpath('//div[@class="biz-main-info embossed-text-white"]/div[2]/span').xpath('string(.)').extract()).replace("\n", "").replace(" ", "")
        elif response.xpath('//div[@class="biz-main-info embossed-text-white"]/div/span/text()'):
            item['forms'] = ''.join(response.xpath('//div[@class="biz-main-info embossed-text-white"]/div/span').xpath('string(.)').extract()).replace("\n", "").replace(" ", "")

        # 描述
        item['description'] = ''.join(response.xpath('//div[@class="from-biz-owner-content"]/p/text()').extract()).replace("\n", "").replace(" ", "")

        # logo图url
        item['logo_imgurl'] = response.meta['logo_imgurl']

        # 经纬度
        location = ''.join(response.xpath('//div[@class="mapbox-map"]/div/@data-map-state').extract())
        location = re.findall('"location": {"latitude": (.*?), "longitude": (.*?)},',location)
        if location:
            item['latitude'] = re.findall("'(.*?)'",str(location))[0]
            item['longitude'] = re.findall("'(.*?)'",str(location))[1]
        else:
            item['latitude'] = ''
            item['longitude'] = ''
        # 背景图
        item['back_img'] = ''.join(response.xpath('//div[@class="js-photo photo photo-1"]/div/a/img/@src').extract())

        yield item
        time.sleep(0.5)