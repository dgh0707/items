# -*- coding: utf-8 -*-
import scrapy
import re,time,os
from taobao.items import TaobaoItem
from urllib import request
import requests


class TbSpider(scrapy.Spider):
    name = 'tb'
    allowed_domains = ['https://pub.alimama.com']
    # urls='https://pub.alimama.com/items/search.json?q=%E9%9B%B6%E9%A3%9F&userType=1&_t=1551230800412&toPage='+str(i)+'&perPageSize=50&auctionTag=&shopTag=&_tb_token_=e097aa3b89ee'
    # start_urls = [urls]
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
        'referer': 'https://pub.alimama.com/promo/search/index.htm?q=%E9%9B%B6%E9%A3%9F&userType=1&_t=1551921904115',
        'cookie': 't=17c09943047b22674001f4068d5fe0c7; cna=BGn+EyBR2WQCAXuLGMrFrvjP; 14604711_yxjh-filter-1=true; account-path-guide-s1=true; undefined_yxjh-filter-1=true; l=bBxh4KGcvHlcl8qpBOfiNuI8aO7t1IOfhsPzw4_GbICPOz1W1o4OWZZGJTYXC3GVa6nMy3yyGx6UBYL3GyUIg; cookie2=1e09900d164afd667b207356e50a4330; v=0; _tb_token_=7e0b37b3e8b35; alimamapwag=TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgNi4xOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvNzIuMC4zNjI2LjEwOSBTYWZhcmkvNTM3LjM2; cookie32=24c4d0a0d61710d515841732a7a881ef; alimamapw=eUt0VxcRDhBoBgdXAgRVUVEBVgwAD1cAB1QCBQUABVAFUVdXAAhTUwc%3D; cookie31=MTQ2MDQ3MTEsTXJDYXJyb3QseXVhbmxlaUBhbWJlcnN0b25lcy5jbixUQg%3D%3D; login=URm48syIIVrSKA%3D%3D; rurl=aHR0cHM6Ly9wdWIuYWxpbWFtYS5jb20v; JSESSIONID=8448534E6A6B7EC2C3FD79DCDC2DB25E; isg=BDs7z1QL48JK8N-cYGUdHRCoyh9lOE_2bBJOsy34HDpRjFtutWLn4wzKpmxnrKeK',

    }

    @staticmethod
    def _clean_str(items):
        for key in items:
            if items[key]:
                items[key] = items[key].strip().replace("\n", "").replace("\r", "").replace("\t", "").replace("\xa0","")
                if items[key] == '':
                    items[key] = None

        return items

    # 添加cookie请求网页
    def start_requests(self):
        # 分页
        for i in range(23,24):
            start_urls = 'https://pub.alimama.com/items/search.json?q=%E9%9B%B6%E9%A3%9F&userType=1&_t=1551921904115&toPage=' + str(
                i) + '&perPageSize=50&auctionTag=&shopTag=&_tb_token_=7e0b37b3e8b35'
            yield scrapy.Request(url=start_urls, callback=self.parse,headers=self.header,dont_filter=True)
        print('-------正在爬取第 %s 页的商品数据--------' % (i,))
        time.sleep(0.5)
    def parse(self,response):
        res= response.text
        # 商品价格
        price_list = re.findall('"zkPrice":(.*?),',res)
        # 商品的比率值
        tkRate_list = re.findall('"tkRate":(.*?),', res)
        # 商品详情页的URL地址
        auctionUrl_list = re.findall('"auctionUrl":"(.*?)",',res)
        for auctionUrl,tkRate,price in zip(auctionUrl_list,tkRate_list,price_list):
            auctionUrl=auctionUrl.replace('http://item.taobao','https://detail.tmall')
            tkRate=tkRate
            price=price
            yield scrapy.Request(auctionUrl, meta={'auctionUrl':auctionUrl,'tkRate': tkRate,'price':price},callback=self.parse1, dont_filter=True,headers=self.header)
        time.sleep(0.5)


    def parse1(self,response):
        res = response.text
        item = TaobaoItem()
        # 商品类型  零食：1
        item['cid'] = '1'
        # 商品的比率值
        item['tkRate'] = response.meta['tkRate']
        # 商品的详情页的URL地址
        auctionUrl = response.meta['auctionUrl']
        item['auctionUrl'] = auctionUrl
        # 商品ID
        item['comm_id'] = auctionUrl.split('=')[-1]
        # 商品名称
        if response.xpath('//div[@class="tb-detail-hd"]/h1/text()').extract_first():
            item['title'] = response.xpath('//div[@class="tb-detail-hd"]/h1/text()').extract_first()
            item['title'] =item['title'].replace("\n", "").replace("\r", "").replace("\t", "")
        elif response.xpath('//div[@id="J_Title"]/h3/text()').extract_first():
            item['title'] = response.xpath('//div[@id="J_Title"]/h3/text()').extract_first()
            item['title'] = item['title'].replace("\n", "").replace("\r", "").replace("\t", "")
        # 商品的价格
        item['price'] = response.meta['price']
        # 商品发货地址
        item['deliveryAdd'] =''.join(re.findall('"prov":"(.*?)",',res))
        # 产品参数
        item['comm_data'] =''.join(response.xpath('//*[@id="J_AttrUL"]/li').extract())

    # 图片下载
        # 商品主图的URL地址
        image_url_list =response.xpath('//*[@id="J_UlThumb"]/li/a/img/@src').extract()
        try:
            os.mkdir('img/' + item['comm_id'])
        except:
            pass

        oss_imgurl_list = []
        i = 0
        for image_url in image_url_list:
            # img_dict['id'] = img_dict['id']+1
            image_url = 'https:'+image_url.replace("_60x60q90.jpg", "")
            request.urlretrieve(image_url,'img/'+item['comm_id']+'/'+image_url.split('/')[-1])
            time.sleep(0.5)
            print('-------正在下载主图图片---------')

        # 拼接OSS的图片地址

            img_dict = {"id":'', "imgurl": "", "status": 0, "describe": ""}
            oss_url = 'https://redbag-imgs.oss-cn-beijing.aliyuncs.com/mall/2019/tmall_img/img/'+item['comm_id']+'/'+image_url.split('/')[-1]+ '?x-oss-process=image/quality,q_60'
            img_dict['imgurl'] = oss_url
            img_dict['id'] = i+1
            i = img_dict['id']
            oss_imgurl_list.append(img_dict)

        item['oss_imgurl'] = str(oss_imgurl_list)
        time.sleep(0.5)

        # 商品的详情图片
        mess_url = 'http://hws.m.taobao.com/cache/wdesc/5.0/?id='+item['comm_id']
        res = requests.get(mess_url, headers=self.header).text
        # if re.findall('<img src="(.*?)" ', res):
        #     mess_img_url = re.findall('<img src="(.*?)" ', res)
        # elif re.findall('<img align="absmiddle" src="(.*?)" ', res):
        #     mess_img_url = re.findall('<img align="absmiddle" src="(.*?)" ', res)
        mess_img_url = re.findall('//img.alicdn.com(.*?).jpg"', res)
        print('商品的ID是：%s' % (item['comm_id'],))
        try:
            os.mkdir('image/' + item['comm_id'])
        except:
            pass

        oss_imageurl_list = []
        i = 0
        for mess_img in mess_img_url:
            img_url = ''.join(mess_img.split('//')[-1])
            img_url = 'https://img.alicdn.com' + img_url + '.jpg'
            # print(img_url)
            # print('========================================================')
            request.urlretrieve(img_url, 'image/' + item['comm_id'] + '/' + img_url.split('/')[-1])
            time.sleep(0.5)
            print('-----正在下载商品详情图片-------')

        # 拼接OSS的详情图的URL地址
            img_dict = {"id": '', "imgurl": "", "status": 0, "describe": ""}
            oss_url = 'https://redbag-imgs.oss-cn-beijing.aliyuncs.com/mall/2019/tmall_img/image/'+ item['comm_id'] + '/' + img_url.split('/')[-1]+ '?x-oss-process=image/quality,q_60'
            img_dict['imgurl'] = oss_url
            img_dict['id'] = i + 1
            i = img_dict['id']
            oss_imageurl_list.append(img_dict)
        item['oss_imageurl'] = str(oss_imageurl_list)
        time.sleep(0.5)

        yield self._clean_str(item)
        print('------正在爬取商品信息--------')
        time.sleep(0.5)

