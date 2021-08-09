import json
import re
from abc import ABC
from html.parser import HTMLParser
from sys import stderr
from traceback import print_exc

from bs4 import BeautifulSoup  # BeautifulSoup4
import requests

def parse_html(html_text):
    class _DeHTMLParser(HTMLParser, ABC):
        def __init__(self):
            HTMLParser.__init__(self)
            self.__text = []

        def handle_data(self, data):
            text = data.strip()
            if len(text) > 0:
                text = re.sub('[ \t\r\n]+', ' ', text)
                self.__text.append(text + ' ')

        def handle_starttag(self, tag, attrs):
            if tag == 'p':
                self.__text.append('\n\n')
            elif tag == 'br':
                self.__text.append('\n')

        def handle_startendtag(self, tag, attrs):
            if tag == 'br':
                self.__text.append('\n')

        def text(self):
            return ''.join(self.__text).strip()

    def dehtml(text):
        try:
            parser = _DeHTMLParser()
            parser.feed(text)
            parser.close()
            return parser.text()
        except:
            print_exc(file=stderr)
            return text

    return dehtml(html_text)

page = 1

headers = {
    'authority': 'search.jd.com',
    'method': 'GET',
    'path': '/s_new.php?keyword=%E8%94%AC%E8%8F%9C&qrst=1&wq=%E8%94%AC%E8%8F%9C&page=13&s=357&click=0',
    'scheme': 'https',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 'pinId=g0lWRjRtWJXGDNDKrimgbQ; rkv=1.0; qrsc=3; unpl=V2_ZzNtbURUSkd8DUUGeUtZUWIAR18RBUBBIVpFXX9NDg0wVhQIclRCFnUUR1ZnGVQUZAAZWUdcRhVFCEdkeBBVAWMDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZHMQVABlBhpYS2dzEkU4dld8Gl4BZTMTbUNnAUEpDUZUeRBYSG8KGlhAUksQfDhHZHg%3d; __jdv=76161171|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_728c842c3c4e42d3bc2eec285ec9fd7d|1616165681569; __jdu=989434948; areaId=14; PCSYCityID=CN_340000_340100_0; shshshfpb=zq8vx9cAW92WNucBcvRsvbQ%3D%3D; shshshfpa=026e7a4e-f040-8509-3029-56b2b537d92e-1607261561; ipLoc-djd=14-1116-3431-57939; pin=jd_fImJCtbXHWws; unick=%E4%B8%8D%E5%96%9C%E6%AC%A2%E5%A4%A7%E6%B5%B7%E7%9A%84%E9%AD%9A; _tp=OVOYdVQ0DrubSUm%2FVx5MsA%3D%3D; _pst=jd_fImJCtbXHWws; user-key=84261171-945f-4370-ad6f-19438f6c8987; cn=0; TrackID=1hFhy6HzNVjCKWjwg4dHkpYRBtjZm7HPhuEGp0ivqs6tmpPVCnpCmacYehz7jPneRoRmrfN3nbaiXy92yoRcvj1ockEJx0FdHwcZO6LuKvmE; ceshi3.com=103; __jda=122270672.989434948.1616165681.1616492013.1616502025.20; __jdc=122270672; shshshfp=f1f830d7a09f10af8607a3e012115a57; __jdb=122270672.5.989434948|20.1616502025; shshshsID=10b70a67cad79ff7002de2048df2b2df_4_1616502220097; thor=55F44C93E2FBD9DE5291AEA1ABF242DF29875E95DFA331F1367758C45E4CF5A15355AE4B17E5DC58DE0A7C2D866FB9220CBA600209C7FC7A0B8ECEE096F065A1E4B4F2A7C903A2BA05959F00CC52A3045AE7E132AB70F8B3970784BCA3C5B628FC8514CA38D9629664DD0208C2F89BEFCE9D280A61281C5ABD7C8DB1BBBD5806EDFE0EFE2B9665B6C04E6E7CC5F942838740C5EB686FFFAC043D4DA09F6BA5A7; 3AB9D23F7A4B3C9B=OA3EA4WZMKY7TQV24DX23QGUX5IJQYOUYJK63NN32QRCWTXI3V37BYZMYSIK3GLR2KOE5KFNTPG26YIVOLSNF6OTMQ',
    'referer': 'https://search.jd.com/Search?keyword=%E8%94%AC%E8%8F%9C&qrst=1&wq=%E8%94%AC%E8%8F%9C&page=13&s=357&click=0',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}

Parameters = {
    'keyword': '蔬菜',
    'qrst': 1,
    'wq': '蔬菜',
    'psort': 3,
    'page': page,
    's': 61,
    'click': 0
}

url = 'https://search.jd.com/s_new.php?keyword=%E8%94%AC%E8%8F%9C&qrst=1&psort=3&wq=%E8%94%AC%E8%8F%9C&psort=3&page=' + str(page) + '&s=61&click=0'

dumpJson = json.dumps(Parameters)

# 正式发送请求，得到返回结果
html = requests.get(url, data=dumpJson, headers=headers).text

soup = BeautifulSoup(html, 'lxml')
# print(soup.prettify())  # prettify()是将html标签语言规范化输出
# a = soup.li.attrs['data-sku']  # soup本身具备标签数属性，标签具备标签内部属性或全部属性的字典形式attrs，返回的是第一个节点

#li_list = list(soup.ul.children)  # children返回的是迭代器类型，可以通过list()转化为列表
li_list = soup.find_all('li')  # 用soup的find_all()函数也可以找到相应的标签返回所有结果存储为list结构

for li in li_list:
    id = li['data-sku']
    name = parse_html(str(li.select('.p-name a')[0]))
    print(name)
