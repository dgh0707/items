import requests
import re
import json
from bs4 import BeautifulSoup

'''main = requests.session()
on_url="https://www.zillow.com/homes/%s_rb/"

headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
    "referer":"https://www.zillow.com/"
}

search=on_url%input("请输入需要搜索的字段:")
def index_url(url):
    url_list=[]
    html1=main.get(url,headers=headers).text
    # print(html1)
    html_soup=BeautifulSoup(html1,"html.parser")

    try:
        html2=html_soup.find_all("ul",attrs={"class":"photo-cards"})[0]
    except:
        print("错误的搜索内容或者搜索不存在")
        return []

    # print(html2)
    html3=html2.find_all("a")
    for html4 in html3:
        url_list.append(html4.attrs["href"])
    url_list.remove('#saved-search-lightbox')

def get_data(url_list):
    for url in url_list:
        html1=main.get(url,headers=headers).text
        html_soup=BeautifulSoup(html1,"html.parser")

        data_group=html_soup.find("div",attrs={"class":"ds-chip"})
        get_money=str(data_group.find("span",attrs={"class":"ds-value"}).string)
        get_bd_ba=data_group.find_all("span",attrs={"class":"ds-vertical-divider ds-bed-bath-living-area"})
        ba_bd_list=[]
        for bad in get_bd_ba:
            bd_ba=bad.find("span",attrs="").string
            ba_bd_list.append(bd_ba)
        try:
            get_bd=str(ba_bd_list[0])+" bd"
        except:
            get_bd=None
        try:
            get_ba=str(ba_bd_list[1])+" ba"
        except:
            get_ba=None

        get_sqft=str(data_group.find("span",attrs={"class":"ds-bed-bath-living-area"}).find("span").string)+" sqft"
        address=data_group.find("h1",attrs={"class":"ds-address-container"}).find_all("span")
        ss=""
        for addr in address:
            ss=ss+str(re.findall("<span>([\S\s]*)</span>",str(addr))[0])
        ss=ss.split(",")
        a1=ss[0]
        a2=ss[1]
        a3=ss[2]
        try:
            zt=data_group.find("span",attrs={"class":"zsg-tooltip-launch_keyword"}).string
        except:
            zt=data_group.find("span",attrs={"class":"ds-status-details"})

        data_group1=html_soup.find("div",attrs={"class":"ds-expandable-card no-footer"})
        time_on_zi=data_group1.find("div",attrs={"class":"ds-overview-stat-value"}).string
        miaoshu=data_group1.find("div",attrs={"class":"character-count-text-fold-container"}).find("div").string

        agent=html_soup.find("div",attrs={"class":"ds-overview-agent-card-container"})

        data_group2=html_soup.find("ul",attrs={"class":"ds-home-fact-list"}).find_all("span",attrs={"class":"ds-body ds-home-fact-value"})
        Type=data_group2[0].string
        Year_built=data_group2[1].string
        try:
            Parking=data_group2[4].string
        except:
            Parking=None
        try:
            lot=data_group2[5].string
        except:
            lot=None

        HOA=html_soup.find("span",attrs={"class":"Text-sc-1vuq29o-0 dvffDA"})


        print(HOA)



        # print(get_money,get_bd,get_ba,get_sqft)

test_list=['https://www.zillow.com/homedetails/Loehr-Rd-Tolland-CT-06084/247207019_zpid/']
get_data(test_list)

# index_url(search)'''

import requests


# inputStr = "1960 Mandela PkwyOakland, CA 94607"
# # 把字符串转换成列表
# str_list = list(inputStr)
#
# # 用循环取出每一个元素
# for i in inputStr:
#     # 判断元素是否是大写
#     if i.isupper():
#         # 如果是大写就记录下标位置
#         index = str_list.index(i)
#         # 修改数据，添加空格
#         str_list.insert(index, " ")
#         # 判断如果是第一个首字母则跳出本次循环
#         if index == 0:
#             continue
#
#         # 转换成字符串
#         outStr = "".join(str_list)
# print(outStr)

import requests,re

url = 'https://www.zillow.com/homes/for_sale/26945893_zpid/'
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
    'cookie': 'zguid=23|%246fc9baf7-7cbf-4b59-93a2-8ae707d21762; _ga=GA1.2.1337783556.1557741018; zjs_user_id=null; _gcl_au=1.1.641618121.1557741062; zjs_anonymous_id=%226fc9baf7-7cbf-4b59-93a2-8ae707d21762%22; __gads=ID=065fcf1a698955b6:T=1557805522:S=ALNI_Mb6LSnQ1vnsSdWhQLjySdAx1nrucg; _gid=GA1.2.1077583517.1558323718; _pxvid=784253dc-7bae-11e9-8176-0242ac120009; ki_r=; ki_s=172156%3A0.0.0.0.2; KruxPixel=true; KruxAddition=true; JSESSIONID=23689072CCE48D708216893FF3D84C31; zgsession=1|dd8b35ae-44d9-4fb0-8fe4-ebafed1c444a; DoubleClickSession=true; ki_t=1558432495076%3B1558662205779%3B1558663048465%3B3%3B7; _px3=d7c98c56bd3e3de11e75df110094e64eed6cf893cb7b6712404412b3ddc74865:qWRxPVGe9DTggcORKSMEZFSogVjPPA/0pE97fwdpnTnkHFH3ohuIgmwgl7CawC3ZJ0pneF36J8jTIpGBr7Uyyg==:1000:tWa3Ef+QGfaJDvhqG6j+V8qVVvkxpkSUHvIBqho1up770d1bbuLGuD765w+UbSIX0226068wfAxTWFRUekZlZidlALGCSM8trNL68BPk/rVnQtPmJRqYwb2BsQS1mogO/UlgN7oy7WbL7GRcR4o/v8ZcIqFS8eWXygDECAAW+XY=; search=6|1561257066573%7Cregion%3DCarrollton-Texas%26rect%3D32.990524%252C-96.8262%252C32.95308%252C-96.973829%26zm%3D12%26zpid%3D26945893%26disp%3Dmap%26mdm%3Dauto%26sort%3Ddays%26lt%3Dfsba%252Cfsbo%252Cfore%252Cnew%252Ccmsn%26fs%3D1%26fr%3D1%26mmm%3D1%26rs%3D0%26ah%3D0%26singlestory%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%09%01%0923482%09%09%092%090%09US_%09; AWSALB=ZSRb5307n9qThDdTVCwF7DBdUQm8egSbdWy3etcsz2V344inrrHQUcggPCWZYJQFf50ktvWJaShQzFq0rvxehWRzJyNgqCAgIcKZ7l3steivrU3r2+JG6sRlHZhH; _gat=1',

}
res = requests.get(url,headers=header).text
print(res)
img = re.findall('"url\":\"https:\\\/\\\/photos.zillowstatic.com\\\/(.*?).jpg',res)
print(img)






















