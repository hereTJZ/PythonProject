import json
import os
import re
import threading
import time
import datetime
import requests
import pandas as pd

from html.parser import HTMLParser
from abc import ABC
from sys import stderr
from traceback import print_exc
from bs4 import BeautifulSoup


# 获取现在的时间（程序开始时间）
starttime = time.time()


# 解析位于商品标题text中的html语言为纯文本内容
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


# 获取需求页面商品id等信息
def get_products():
    products_list = []
    page = 1

    while True:
        print("===================")
        print("获取第" + str(page) + "页商品id等信息~")
        print("===================")

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

        url = 'https://search.jd.com/s_new.php?keyword=%E8%94%AC%E8%8F%9C&qrst=1&psort=3&wq=%E8%94%AC%E8%8F%9C&psort=3&page=' + str(
            page) + '&s=61&click=0'

        dumpJson = json.dumps(Parameters)


        try:
            # 正式发送请求，得到返回结果
            html = requests.get(url, data=dumpJson, headers=headers).text

            soup = BeautifulSoup(html, 'lxml')
            # print(soup.prettify())  # prettify()是将html标签语言规范化输出
            # a = soup.li.attrs['data-sku']  # soup本身具备标签数属性，标签具备标签内部属性或全部属性的字典形式attrs，返回的是第一个节点

            # li_list = list(soup.ul.children)  # children返回的是迭代器类型，可以通过list()转化为列表
            li_list = soup.find_all('li')  # 用soup的find_all()函数也可以找到相应的标签返回所有结果存储为list结构

            for li in li_list:
                id = li['data-sku']
                name = parse_html(str(li.select('.p-name a')[0]))
                price = parse_html(str(li.select('.p-price i')[0]))

                # 查重
                for i in range(len(products_list)):
                    if id == products_list[i]:
                        continue

                # 获取该商品的总体评价信息
                summary = get_comment_summary(id)
                time.sleep(0.2)

                product = {
                    "id": id,
                    "name": name,
                    "price": price,

                    "comment_num": summary['comment_num'],
                    "average_score": summary['average_score'],
                    "good_rate": summary['good_rate'],
                    "general_rate": summary['general_rate'],
                    "poor_rate": summary['poor_rate'],
                    "hot_tags": summary['hot_tags'],

                    "product_url": "https://item.jd.com/" + str(id) + ".html",
                }
                # 结果追加入商品列表中
                products_list.append(product)

                if len(products_list) == 100:
                    print("===成功获取" + str(page - 1) + "页商品id等信息===")
                    print(products_list)
                    return products_list

        except:
            print("~~~~~~~~~~~~")
            print("休息5s！")
            time.sleep(5)

        page += 1


num = 1
# 获取商品评价总体信息 100个
def get_comment_summary(id):
    global num
    print(">>>>>> " + str(num) + "、获取商品：" + str(id) + "评价总体信息 <<<<<<")
    num+=1

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'pinId=g0lWRjRtWJXGDNDKrimgbQ; unpl=V2_ZzNtbURUSkd8DUUGeUtZUWIAR18RBUBBIVpFXX9NDg0wVhQIclRCFnUUR1ZnGVQUZAAZWUdcRhVFCEdkeBBVAWMDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZHMQVABlBhpYS2dzEkU4dld8Gl4BZTMTbUNnAUEpDUZUeRBYSG8KGlhAUksQfDhHZHg%3d; __jdv=76161171|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_728c842c3c4e42d3bc2eec285ec9fd7d|1616165681569; __jdu=989434948; areaId=14; PCSYCityID=CN_340000_340100_0; shshshfpb=zq8vx9cAW92WNucBcvRsvbQ%3D%3D; shshshfpa=026e7a4e-f040-8509-3029-56b2b537d92e-1607261561; shshshfp=f1f830d7a09f10af8607a3e012115a57; ipLoc-djd=14-1116-3431-57939; jwotest_product=99; mba_muid=989434948; TrackID=1ZoYdWmAMkooptv0iTGcKsfbRsw94ZYLHbFHrerFh4YMhze-ntzzNoxE4emkEGOOHcFlS-DbWMPFTbo4wdAe900RzX93CIvHEvwTmsv3nCf4; pin=jd_fImJCtbXHWws; unick=%E4%B8%8D%E5%96%9C%E6%AC%A2%E5%A4%A7%E6%B5%B7%E7%9A%84%E9%AD%9A; _tp=OVOYdVQ0DrubSUm%2FVx5MsA%3D%3D; _pst=jd_fImJCtbXHWws; __jd_ref_cls=Mnpm_ComponentApplied; __jdc=122270672; wlfstk_smdl=ca83va5lcpakkosswjrwptwp3saj4nxh; shshshsID=792a7500592047e1b3c673269ec129b1_1_1616303003236; __jda=122270672.989434948.1616165681.1616296948.1616303003.5; __jdb=122270672.1.989434948|5.1616303003; 3AB9D23F7A4B3C9B=OA3EA4WZMKY7TQV24DX23QGUX5IJQYOUYJK63NN32QRCWTXI3V37BYZMYSIK3GLR2KOE5KFNTPG26YIVOLSNF6OTMQ; JSESSIONID=4C7E6855D329CFC8CC0C988A9D88CFA1.s1',
        'Host': 'club.jd.com',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
    }

    Parameters = {
        'callback': 'fetchJSON_comment98',
        'productId': id,
        'score': 0,
        'sortType': 5,
        'page': 0,
        'pageSize': 10,
        'isShadowSku': 0,
        'fold': 1
    }

    url = "https://club.jd.com/comment/skuProductPageComments.action?callback=fetchJSON_comment98&productId=" + str(id) + "&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1"

    while True:
        try:
            dumpJson = json.dumps(Parameters)
            # 正式发送请求，得到返回结果
            response = requests.get(url, data=dumpJson, headers=headers).text

            pattern = re.compile(r"[(](.*)[)]")
            string = re.findall(pattern, response)[0]  # 返回的结果是字符串

            # 将字符类型数据转换为json字典
            datas = json.loads(string)

            # 拼接热评标签
            hot_tags = ""
            for i in datas['hotCommentTagStatistics']:
                hot_tags += i['name'] + '、'

            # 该商品评论的总结信息，只需要获取一次
            result = {
                "comment_num": datas['productCommentSummary']['commentCountStr'],
                "average_score": datas['productCommentSummary']["averageScore"],
                "good_rate": str(datas['productCommentSummary']["goodRateShow"]) + "%",
                "general_rate": str(datas['productCommentSummary']["generalRateShow"]) + "%",
                "poor_rate": str(datas['productCommentSummary']["poorRateShow"]) + "%",
                "hot_tags": hot_tags.strip('、')
            }

            return result

        except:
            print("总结信息获取失败！！！休息3秒后重新尝试")
            time.sleep(3)


# 获取各商品有效评论内容
def get_comments(id, isFold):
    print("=================================================================")
    print("                       商品：" + str(id))
    print("=================================================================")

    # 评论页数
    page = 0
    # 总计评论数
    count = 0
    # 评论结果列表
    result_list = []

    fail_num = 0

    while True:

        # 判断是否是折叠评论
        if isFold:
            headers = {
                'Accept': "*/*",
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Cookie': 'pinId=g0lWRjRtWJXGDNDKrimgbQ; unpl=V2_ZzNtbURUSkd8DUUGeUtZUWIAR18RBUBBIVpFXX9NDg0wVhQIclRCFnUUR1ZnGVQUZAAZWUdcRhVFCEdkeBBVAWMDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZHMQVABlBhpYS2dzEkU4dld8Gl4BZTMTbUNnAUEpDUZUeRBYSG8KGlhAUksQfDhHZHg%3d; __jdv=76161171|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_728c842c3c4e42d3bc2eec285ec9fd7d|1616165681569; __jdu=989434948; areaId=14; PCSYCityID=CN_340000_340100_0; shshshfpb=zq8vx9cAW92WNucBcvRsvbQ%3D%3D; shshshfpa=026e7a4e-f040-8509-3029-56b2b537d92e-1607261561; ipLoc-djd=14-1116-3431-57939; jwotest_product=99; pin=jd_fImJCtbXHWws; unick=%E4%B8%8D%E5%96%9C%E6%AC%A2%E5%A4%A7%E6%B5%B7%E7%9A%84%E9%AD%9A; _tp=OVOYdVQ0DrubSUm%2FVx5MsA%3D%3D; _pst=jd_fImJCtbXHWws; user-key=84261171-945f-4370-ad6f-19438f6c8987; cn=0; ceshi3.com=103; TrackID=1-96R5ginZZPUAsgcuGlFZgxKFhv9A05spw65QTrjlGaSYX23ckF_JAtscSKYCDS_PlzzjRDstHgMwKo6AWx5je6BqbRIdy2BK7s-ens2UAM; __jdc=122270672; shshshfp=f1f830d7a09f10af8607a3e012115a57; wlfstk_smdl=45bjmu7hkocpdt88fg9s8qf1uq4x3408; __jda=122270672.989434948.1616165681.1616545233.1616552992.25; thor=55F44C93E2FBD9DE5291AEA1ABF242DF29875E95DFA331F1367758C45E4CF5A1FB214622549EA91983D4CDE482E53F8840E82895F5FF1AAB4B6C829B92AC00CF5F16EE11CDC26B837413540EFE9C433A25CA877BD42161692ECFEFCE51F2527B9D7E2EBFB2E2DE3D7875555F73FC8571F5FE777721B91345E92DE5FEBCAAA03AEE68EFCC080A97042F34251C51A0F7E4B4EE54298D9689788C70318707816F0B; __jdb=122270672.4.989434948|25.1616552992; shshshsID=65f5df3137a90451bf0a2676887fa6b5_4_1616553172405; 3AB9D23F7A4B3C9B=OA3EA4WZMKY7TQV24DX23QGUX5IJQYOUYJK63NN32QRCWTXI3V37BYZMYSIK3GLR2KOE5KFNTPG26YIVOLSNF6OTMQ; JSESSIONID=ABD330FC498AB11D08BF3716B52C4783.s1',
                'Referer': 'https://item.jd.com/',
                'Host': 'club.jd.com',
                'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'Sec-Fetch-Dest': 'script',
                'Sec-Fetch-Mode': 'no-cors',
                'Sec-Fetch-Site': 'same-site',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
            }

            Parameters = {
                'callback': 'jQuery1046740',
                'productId': id,
                'score': 0,
                'sortType': 5,
                'page': page,
                'pageSize': 5,
                '_': '1616553634362'
            }

            url = "https://club.jd.com/comment/getProductPageFoldComments.action?callback=jQuery1046740&" \
                  "productId=" + str(id) + "&score=0&sortType=5&" \
                                           "page=" + str(page) + "&pageSize=5&_=1616553634362"

        # 非折叠评论
        else:
            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Cookie': 'pinId=g0lWRjRtWJXGDNDKrimgbQ; unpl=V2_ZzNtbURUSkd8DUUGeUtZUWIAR18RBUBBIVpFXX9NDg0wVhQIclRCFnUUR1ZnGVQUZAAZWUdcRhVFCEdkeBBVAWMDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZHMQVABlBhpYS2dzEkU4dld8Gl4BZTMTbUNnAUEpDUZUeRBYSG8KGlhAUksQfDhHZHg%3d; __jdv=76161171|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_728c842c3c4e42d3bc2eec285ec9fd7d|1616165681569; __jdu=989434948; areaId=14; PCSYCityID=CN_340000_340100_0; shshshfpb=zq8vx9cAW92WNucBcvRsvbQ%3D%3D; shshshfpa=026e7a4e-f040-8509-3029-56b2b537d92e-1607261561; ipLoc-djd=14-1116-3431-57939; jwotest_product=99; pin=jd_fImJCtbXHWws; unick=%E4%B8%8D%E5%96%9C%E6%AC%A2%E5%A4%A7%E6%B5%B7%E7%9A%84%E9%AD%9A; _tp=OVOYdVQ0DrubSUm%2FVx5MsA%3D%3D; _pst=jd_fImJCtbXHWws; user-key=84261171-945f-4370-ad6f-19438f6c8987; cn=0; ceshi3.com=103; TrackID=1-96R5ginZZPUAsgcuGlFZgxKFhv9A05spw65QTrjlGaSYX23ckF_JAtscSKYCDS_PlzzjRDstHgMwKo6AWx5je6BqbRIdy2BK7s-ens2UAM; __jdc=122270672; shshshfp=f1f830d7a09f10af8607a3e012115a57; wlfstk_smdl=45bjmu7hkocpdt88fg9s8qf1uq4x3408; __jda=122270672.989434948.1616165681.1616545233.1616552992.25; thor=55F44C93E2FBD9DE5291AEA1ABF242DF29875E95DFA331F1367758C45E4CF5A1FB214622549EA91983D4CDE482E53F8840E82895F5FF1AAB4B6C829B92AC00CF5F16EE11CDC26B837413540EFE9C433A25CA877BD42161692ECFEFCE51F2527B9D7E2EBFB2E2DE3D7875555F73FC8571F5FE777721B91345E92DE5FEBCAAA03AEE68EFCC080A97042F34251C51A0F7E4B4EE54298D9689788C70318707816F0B; __jdb=122270672.4.989434948|25.1616552992; shshshsID=65f5df3137a90451bf0a2676887fa6b5_4_1616553172405; JSESSIONID=6675E83BF582F386B6AD6FEE505132A2.s1; 3AB9D23F7A4B3C9B=OA3EA4WZMKY7TQV24DX23QGUX5IJQYOUYJK63NN32QRCWTXI3V37BYZMYSIK3GLR2KOE5KFNTPG26YIVOLSNF6OTMQ',
                'Host': 'club.jd.com',
                'Referer': 'https://item.jd.com/',
                'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'Sec-Fetch-Dest': 'script',
                'Sec-Fetch-Mode': 'no-cors',
                'Sec-Fetch-Site': 'same-site',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
            }

            Parameters = {
                'callback': 'fetchJSON_comment98',
                'productId': id,
                'score': 0,
                'sortType': 5,
                'page': page,
                'pageSize': 10,
                'isShadowSku': 0,
                'rid': 0,
                'fold': 1
            }

            url = "https://club.jd.com/comment/productPageComments.action?" \
              "callback=fetchJSON_comment98&" \
              "productId=" + str(id) + "&" \
                                       "score=0&" \
                                       "sortType=5&" \
                                       "page=" + str(page) + "&" \
                                                             "pageSize=10&" \
                                                             "isShadowSku=0&" \
                                                             "rid=0&fold=1"


        try:
            print("第" + str(page + 1) + "页评论~")

            dumpJson = json.dumps(Parameters)
            # 正式发送请求，得到返回结果
            response = requests.get(url, data=dumpJson, headers=headers).text

            pattern = re.compile(r"[(](.*)[)]")
            string = re.findall(pattern, response)[0]  # 返回的结果是字符串

            # 将字符类型数据转换为json字典
            datas = json.loads(string)

            comments_list = datas["comments"]
            # 记录评论数：
            count += len(comments_list)

            # 遍历每页的评论
            for comment in comments_list:
                # 需要的返回结果封装成result字典对象
                result = {
                    'user_name': comment['nickname'],
                    'score': comment['score'],
                    'content': comment['content'],
                    'time': comment['creationTime'],
                    'after_comment': '',
                    'after_time': '',
                    'time_interval': '',  # 追评时间间隔，单位：天
                    'reply': ''
                }

                # 追评
                try:
                    result['after_comment'] = comment['afterUserComment']['content']
                    result['after_time'] = comment['afterUserComment']['created']
                    t1 = datetime.datetime.strptime(result['time'], '%Y-%m-%d %H:%M:%S')
                    t2 = datetime.datetime.strptime(result['after_time'], '%Y-%m-%d %H:%M:%S')
                    time_interval = t2 - t1
                    result['time_interval'] = str(time_interval)
                    print("追评：" + result['after_comment'] + "    |    时间：" + result['after_time'] + "    |    间隔：" + result['time_interval'])
                except:
                    pass

                # 回复
                try:
                    replies = ''
                    for reply in comment['replies']:
                        replies += (str(comment['replies'].index(reply) + 1) + "、" + reply['content'] + "(" + reply['creationTime'] + ")\n")

                    result['reply'] = replies
                    print("店家回复：" + replies)
                except:
                    pass

                result_list.append(result)


            # 当没有评论时，结束评论获取
            if len(comments_list) == 0 or count == 10000:
                print("商品：" + str(id) + "所有评论爬取完毕！！")
                print("该线程评论共计：" + str(count) + "条")
                final = {
                    'result_list': result_list,
                    'count': count
                }
                return final

            print(comments_list)
            page += 1
            fail_num = 0

        except:
            fail_num += 1
            print("------------------")
            print("请求过快，休息3秒！！！")
            print("------------------")
            time.sleep(3)

            if fail_num > 6:
                print("。。。。。。。。。。。。。。。。。。。。。。。。。。。。。")
                print("连续请求失败超过6次，暂停30s~")
                time.sleep(30)


# 继承父类threading.Thread，定义带返回值的线程类
class MyThread(threading.Thread):
    # Python的’构造函数‘，自由添加需要的参数
    def __init__(self, ID, isFold, name):
        threading.Thread.__init__(self)
        self.threadID = ID
        self.name = name
        self.isFold = isFold

    # 把要执行的代码写到run函数里面，线程在创建后会直接运行run函数
    def run(self):
        print("启动线程：" + self.name)
        self.result = get_comments(self.threadID, self.isFold)
        print("结束线程：" + self.name)

    # 该方法获取线程函数的返回值
    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # 在项目路径下建立存储评论的文件夹
    if not os.path.exists(r'comments'):
        os.mkdir(r'comments')
        print('当前路径下创建comments文件夹成功！')
    else:
        print('当前路径下已存在comments文件夹！')


    # 获取需求页面商品id等信息
    products_list = get_products()
    df = pd.DataFrame(products_list)
    df.rename(
        columns={
            "id": "商品id",
            "name": "商品名称",
            "comment_num": "评论数",
            "average_score": "总评分",
            "good_rate": "好评率",
            "general_rate": "中评率",
            "poor_rate": "差评率",
            "hot_tags": "热门标签",
            "product_url": "商品链接"
        },
        inplace=True
    )

    save_path = r'comments/商品统计.xlsx'
    df.to_excel(save_path, index=False)  # 保存为xlsx文件（Excel文件），行索引去除
    print("========================商品信息保存成功========================")


    # # 从已保存的表中读取商品数据
    # sheet = pd.read_excel(save_path)  # 读取列表为Dataframe结构数据
    # sheet.rename(
    #     columns={
    #             "商品id": "id",
    #             "商品名称": "name",
    #             "评论数": "comment_num",
    #             "总评分": "average_score",
    #             "好评率": "good_rate",
    #             "中评率": "general_rate",
    #             "差评率": "poor_rate",
    #             "热门标签": "hot_tags",
    #             "商品链接": "product_url"
    #         },
    #         inplace=True
    # )
    # products_list = sheet.to_dict('records')
    # # print(products_list)
    # # read_uid = sheet.loc[ : , :'商品id']  # 选取属性名为 商品id 的数据(先行后列规则)


    # 统计总评论数
    number = 0
    # 遍历商品列表
    for product in products_list:
        order = products_list.index(product) + 1  # 线程序号

        # if order < 91:
        #     continue

        print(product)
        u =1
        t1 = MyThread(product['id'], False, 'comment_thread-' + str(order))
        t2 = MyThread(product['id'], True, 'fold_comment_thread-' + str(order))

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        result1 = t1.get_result()
        result2 = t2.get_result()
        number += result1['count'] + result2['count']
        result_list = result1['result_list'] + result2['result_list']

        df = pd.DataFrame(result_list)
        df.rename(
            columns={
                'user_name': '用户',
                'score': '评分',
                'content': '评论内容',
                'time': '初评时间',
                'after_comment': '追评内容',
                'after_time': '追评时间',
                'time_interval': '追评时间间隔',  # 追评时间间隔，单位：天
                'reply': '店家回复'
            },
            inplace=True
        )

        # 保存文件时去除文件名中的非法字符
        illegal_pattern = re.compile('[/\\\:*?\"<>|]')
        product_name = re.sub(illegal_pattern, ' ', str(product['name']))
        save_path = r'comments/' + product_name + '.xlsx'
        df.to_excel(save_path, index=False)  # 保存为xlsx文件（Excel文件），行索引去除
        print("========================商品" + str(product['id']) + "评论保存成功========================")



    # 统计时间与数量
    endtime = time.time()  # 获取现在的时间（程序结束时间）
    print('所有评论数目共计：' + str(number) + '个\n')
    print('本次爬取耗时：' + str(endtime - starttime) + '秒')

