# -*- coding: utf-8 -*-
import scrapy
from urllib import request
import json,os,time,datetime
from toutiao.items import ToutiaoItem


class TtSpider(scrapy.Spider):
    name = 'tt'
    allowed_domains = ['www.jinse.com']
    start_urls = ['https://api.jinse.com/v5/information/list?catelogue_key=www&limit=23&information_id=0&flag=down&version=9.9.9']

    @staticmethod
    def _clean_str(items):
        for key in items:
            if items[key]:
                items[key] = items[key].strip().replace("', '", "").replace("['", "").replace("']", "").replace("\xa0","").replace(
                "\uf0d8", "").replace("\\xa0", "").replace("\\u3000", "").replace('金色财经', '资本未来').replace('金色', '资本未来')
                if items[key] == '':
                    items[key] = None

        return items
    def parse(self, response):
        html = json.loads(response.text)

        # 列表内容
        list = html['list']
        for i in list:
            article_id = i['id']

            try:
                url = i['extra']['topic_url']
            except:
                pass
            #获取时间
            try:
                published_time = i['extra']['published_at']
            except:
                pass
            time_array = time.localtime(published_time)
            publish_time = time.strftime("%Y-%m-%d/%H:%M:%S", time_array)
            #获取浏览量
            try:
                read_number = i['extra']['read_number']
            except:
                pass
            #获取导读内容
            try:
                summary = i['extra']['summary']
            except:
                pass

            yield scrapy.Request(url,meta={'article_id':article_id,'publish_time': publish_time, 'read_number': read_number, 'summary': summary},
                                 callback=self.parse1, dont_filter=True)
            time.sleep(1)
        # 下一分页的ID
        bottom_id = html['bottom_id']
        bottom_url = 'https://api.jinse.com/v5/information/list?catelogue_key=www&limit=23&information_id=' + str(bottom_id) + '&flag=down&version=9.9.9'
        yield scrapy.Request(bottom_url, callback=self.parse, dont_filter=True)
        time.sleep(1)

    def parse1(self,response):
        items = ToutiaoItem()

        #类型
        items['class_id']='1'
        # 文章ID
        items['article_id'] = str(response.meta['article_id'])
        #标题
        items['title'] = response.xpath('//*[@id="app"]/div[1]/div/div[1]/div/div[1]/h2').xpath('string(.)').extract_first()
        #作者
        items['writer']=response.xpath('//*[@id="app"]/div[1]/div/div[1]/div/div[2]/a').xpath('string(.)').extract_first()
        #发表时间
        items['publish_time'] = str(response.meta['publish_time'])

        # 浏览量
        items['read_number'] = str(response.meta['read_number'])
        # 导读
        items['summary'] = str(response.meta['summary'])
        #内容
        if response.css('div.js-article-detail p').extract():
            article = response.css('div.js-article-detail p').extract()
            article = ''.join(article)

        #关键字
        try:
            tags=response.xpath('//div[@class="tags"]/a').xpath('string(.)').extract()
            items['tags'] =','.join(tags)
        except:
            pass
        time.sleep(1)


    #图片下载
        # 根据日期创建文件夹
        file_day = items['publish_time'].split('/')[0]
        try:
            os.mkdir('img/tt_img/' + file_day)
        except:
            pass
        time.sleep(1)
        # 遍历img文件夹下的所有日期文件夹
        path = r'E:\安培斯通\amber-spider\\toutiao\img\\tt_img'
        # path = r'/home/amber-spider/toutiao/img/tt_img'
        date_files = os.listdir(path)
        for file in date_files:
            fi = os.path.join(path, file)
            fil = os.path.join(path, file).split('/')[-1]

            if fil == file_day:
                try:
                    os.mkdir(fi +'/' + items['article_id'])
                except:
                    pass
                if response.css('div.js-article-detail p img::attr(src)').extract():
                    img_url = response.css('div.js-article-detail p img::attr(src)').extract()
                time.sleep(1)
                try:
                    for i in img_url:

                        #截取原图的URL地址
                        url=i.split('_')[0]

                        request.urlretrieve(url, fi +'/' + items['article_id'] + '/' + url.split("/")[-1]+'.jpg')
                        time.sleep(1)
                except:
                    pass

            # 拼接oss上传路径
                oss_url = 'https://capital-future-imgs.oss-cn-beijing.aliyuncs.com/tt_img/' + fil + '/' + items[
                    'article_id'] + '/'
                if 'https://img.jinse.com/' and '_image3.png' in article:
                    items['article'] = article.replace('https://img.jinse.com/', oss_url).replace(
                        '_image3.png', '.jpg?x-oss-process=image/resize,l_500')
                elif 'https://img.jinse.com/' and '_watermarknone.png' in article:
                    items['article'] = article.replace('https://img.jinse.com/', oss_url).replace(
                        '_watermarknone.png', '.jpg?x-oss-process=image/resize,l_500')
                else:
                    items['article'] = article
            # 内容里的图片地址
                if 'https://capital-future-imgs.oss-cn-beijing.aliyuncs.com/' in items['article']:
                    oss_url1 = items['article'].split('src=')[1].split('.jpg')[0].replace('"','') + '.jpg?x-oss-process=image/resize,l_500'
                    items['oss_url1'] = oss_url1
                else:
                    items['oss_url1'] = 'https://capital-future-imgs.oss-cn-beijing.aliyuncs.com/images/new_default.png?x-oss-process=image/resize,l_500'

                yield self._clean_str(items)

    # 根据时间终止爬虫
        # 爬取时间
        array_time1 = time.strptime(items['publish_time'], "%Y-%m-%d/%H:%M:%S")
        crawl_time = time.mktime(array_time1)
        # 获取当前时间戳
        now = datetime.datetime.now()
        # 当前时间减去1天(1天=86400秒)
        sched_timer = str(datetime.datetime(now.year, now.month, now.day, now.hour, now.minute,
                                            now.second) - datetime.timedelta(seconds=86400*5))
        array_time = time.strptime(sched_timer, "%Y-%m-%d %H:%M:%S")
        now_time = time.mktime(array_time)
        if crawl_time < now_time:
            self.crawler.stop()
