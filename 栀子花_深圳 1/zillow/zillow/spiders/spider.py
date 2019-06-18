# -*- coding: utf-8 -*-
import re
import time

import scrapy
from zillow.items import ZillowItem


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['www.zillow.com']
    # start_urls = ['http://https://www.zillow.com/']

    def start_requests(self):
        i=2
        start_urls = 'https://www.zillow.com/homes/lease_rb/'+str(i)+'_p/'
        yield scrapy.Request(url=start_urls, callback=self.parse, dont_filter=True)
        time.sleep(1)

    def parse(self, response):
        aurl_list = re.findall('"detailUrl":"(.*?)",',response.text)[0:1]
        for aurl in aurl_list:
            yield scrapy.Request(url=aurl, callback=self.parse1,
                                 meta={ 'aurl': aurl}, dont_filter=True)
            time.sleep(0.5)

    def parse1(self,response):
        print(response.text)

        # img = re.findall('"url":"https://photos.zillowstatic.com/(.*?).jpg', response.text)
        # print(img)
        print(response.meta['aurl'])
        item = ZillowItem()
        # 详情页地址
        item['aurl'] = response.meta['aurl']
        # 价格
        if response.xpath('//*[@id="home-details-content"]/div/div/div[3]/div[3]/div[1]/div/div[1]/div/div/h3/span/span/text()'):
            item['price'] = response.xpath('//*[@id="home-details-content"]/div/div/div[3]/div[3]/div[1]/div/div[1]/div/div/h3/span/span[1]/text()').extract_first().replace('$','')
        elif response.xpath('//*[@id="home-value-wrapper"]/div/div[2]/span/text()'):
            item['price'] = response.xpath('//*[@id="home-value-wrapper"]/div/div[2]/span/text()').extract_first().replace('$','')

        h3_list = response.xpath('//div[@class="ds-chip"]/div/div/div/div/header/h3/span/span[1]/text()').extract()
        # 卧室
        item['room'] = h3_list[0]
        # 浴室
        item['bath'] = h3_list[1]
        # 活动面积
        item['living_area'] = h3_list[2]
        # 详细地址列表
        addres_list = response.xpath('//*[@id="home-details-content"]/div/div/div[3]/div[3]/div[1]/div/div[2]/header/h1/span/text()').extract()
        # 地址
        item['addres'] = addres_list[0]
        # 城市
        item['city'] = addres_list[2].split(',')[0]
        # 州
        item['state'] = addres_list[2].split(',')[-1].split(' ')[1]
        # 邮编
        item['postcode'] = addres_list[2].split(',')[-1].split(' ')[-1]
        # 租赁类型
        item['rent'] = response.xpath('//*[@id="ds-chip-removable-content"]/div[1]/span/text()').extract_first()
        # 时间
        item['days'] = response.xpath('//*[@id="ds-data-view"]/ul/li[1]/div/div/div[1]/div[1]/ul/li[1]/div[2]/text()').extract_first()
        # 房屋类型
        type_room_list = response.xpath('//*[@id="ds-data-view"]/ul/li[2]/div/div/div[1]/ul/li/span/text()').extract()
        l1 = type_room_list[::2]
        l2 = type_room_list[1::2]
        ll = []
        for i in range(len(l1)):
            ll.append(l1[i] + l2[i])
        for i in ll:
            if 'Type' in i:
                item['type_room'] = i.split(':')[-1]

            if 'Year built' in i:
                item['year_built'] = i.split(':')[-1]
            else:
                item['year_built'] = ''
            if 'Parking' in i:
                item['parking'] = i.split(':')[-1]
            else:
                item['parking'] = ''
            if 'Lot' in i:
                item['lot'] = i.split(':')[-1]
            else:
                item['lot'] = ''
        # 图片URL
        item['img_url'] = response.xpath('//*[@id="yui_3_18_1_1_1558596544362_10633"]/li/picture/img/@src').extract()
        # 联系人
        item['name'] = response.xpath('//*[@id="yui_3_18_1_1_1558596544362_19995"]/text()').extract()
        # 联系方式
        item['phone'] = response.xpath('//*[@id="yui_3_18_1_1_1558596544362_19997"]/li[2]/text()').extract()




        # yield item

