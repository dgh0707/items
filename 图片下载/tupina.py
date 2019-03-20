'''
图片下载，输入关键字想下载什么图片就下载什么图片，并且保存到电脑上、

所需要的模块：
    os，re，requests
'''
import requests
import re,os

word=input('请输入你要爬取的图片类名：')
if not os.path.exists(word):
    os.mkdir(word)
# 将原页面的URL地址的index换成flip就可以使瀑布流转换为分页
url = 'http://image.baidu.com/search/flip?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=index&fr=&hs=0&xthttps=000000&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word='+str(word)+'&oq='+str(word)+'&rsp=-1'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}
response = requests.get(url,headers = headers)
res = response.content.decode()

# 获取图片的URL
resurl=re.findall('"objURL":"(.*?)"',res)
print(resurl)

# 下载图片到电脑
for i in resurl:
    name = i.split('/')[-1].replace(' ', '').replace('?', '')
    r = requests.get(i, headers=headers)
    print(i, name)
    with open(word +'/' + name + '.jpg', 'wb') as f:
        f.write(r.content)
