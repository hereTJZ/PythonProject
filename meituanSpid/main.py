import json
import os
import re
import threading
import time
import datetime
import random
import requests
import pandas as pd

from html.parser import HTMLParser
from abc import ABC
from sys import stderr
from traceback import print_exc
from bs4 import BeautifulSoup

# 获取现在的时间（程序开始时间）
starttime = time.time()

shop_number = 0
comment_number = 0


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


# 获取所有店铺信息
def get_shops():
    page = 1
    shops_list = []
    global shop_number

    fail_num = 0
    while True:
        print('---正在爬取第' + str(page) + '页的店铺---')

        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': 'uuid=38314cfb231e4bae92a1.1616510460.1.0.0; _lxsdk_cuid=1785f88293ac8-01081aada60609-57442618-144000-1785f88293a2e; mtcdn=K; userTicket=IzLfYYFURpSASVtmoQPspAMQwnQrSUiOrnrSQGwC; lsu=; IJSESSIONID=node0ym3w4jht3jzdk433keuc0f8v21172912; iuuid=BBCD032121B47E9011B614A417D2542E9FC2295BA15D433DD5A4530955DE54E6; webp=1; _lxsdk=BBCD032121B47E9011B614A417D2542E9FC2295BA15D433DD5A4530955DE54E6; __utma=74597006.188086389.1616578855.1616578855.1616578855.1; __utmc=74597006; __utmz=74597006.1616578855.1.1.utmcsr=link.csdn.net|utmccn=(referral)|utmcmd=referral|utmcct=/; ci3=1; _lx_utm=utm_source%3Dlink.csdn.net%26utm_medium%3Dreferral%26utm_content%3D%252F; _hc.v=4af2f92a-0daa-68cc-2adf-a9fc8875e576.1616579481; ci=42; cityname=%E8%A5%BF%E5%AE%89; a2h=4; latlng=31.798445,117.20522,1616581341775; i_extend=Gimthomepagecategory122H__a100016__b1; rvct=42%2C20%2C1; lt=KaKoeVhJcIUGGB81r_1lC0Pi7EsAAAAAJg0AAD7lUunA5AgrbDOEGVemHcaDbLM_S3IWUb3TvSQqIqrZbE4FtF1QKLNBREPSG6_2mQ; u=2562897915; n=%E4%B8%8D%E5%96%9C%E6%AC%A2%E5%A4%A7%E6%B5%B7%E7%9A%84%E9%AD%9A; token2=KaKoeVhJcIUGGB81r_1lC0Pi7EsAAAAAJg0AAD7lUunA5AgrbDOEGVemHcaDbLM_S3IWUb3TvSQqIqrZbE4FtF1QKLNBREPSG6_2mQ; firstTime=1616590277300; unc=%E4%B8%8D%E5%96%9C%E6%AC%A2%E5%A4%A7%E6%B5%B7%E7%9A%84%E9%AD%9A; _lxsdk_s=1786445f21a-546-e01-823%7C%7C3',
            'Host': 'apimobile.meituan.com',
            'Origin': 'https://xa.meituan.com',
            'Referer': 'https://xa.meituan.com/',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
        }

        parameter = {
            'uuid': '38314cfb231e4bae92a1.1616510460.1.0.0',
            'userid': 2562897915,
            'limit': 32,
            'offset': 32 * (page - 1),
            'cateId': 21004,
            'token': 'KaKoeVhJcIUGGB81r_1lC0Pi7EsAAAAAJg0AAD7lUunA5AgrbDOEGVemHcaDbLM_S3IWUb3TvSQqIqrZbE4FtF1QKLNBREPSG6_2mQ',
            'areaId': -1
        }

        url = 'https://apimobile.meituan.com/group/v4/poi/pcsearch/42?uuid=38314cfb231e4bae92a1.1616510460.1.0.0&userid=2562897915&limit=32&' \
              'offset=' + str(32 * (page - 1)) + \
              '&cateId=21004&token=KaKoeVhJcIUGGB81r_1lC0Pi7EsAAAAAJg0AAD7lUunA5AgrbDOEGVemHcaDbLM_S3IWUb3TvSQqIqrZbE4FtF1QKLNBREPSG6_2mQ&areaId=-1'


        try:
            dumpJson = json.dumps(parameter)

            response = requests.get(url, data=dumpJson, headers=headers).text

            object = json.loads(response)

            datas = object['data']['searchResult']
            if len(datas) == 0:
                print('==================================\n 所有门店信息获取完成！！！\n==================================')
                break

            for data in datas:
                shop = {
                    'id': data['id'],
                    'name': data['title'],  # 门店名称
                    'price': data['avgprice'],  # 人均价格￥
                    'score': data['avgscore'],  # 评分
                    'commentNum': data['comments'],  # 评论数
                    'tag': data['backCateName'] + '|' + data['areaname'],  # 门店标签
                    'address': data['address'],  # 门店地址
                    'url': 'https://www.meituan.com/jiankangliren/' + str(data['id']) + '/',  # 链接
                }

                shops_list.append(shop)
                shop_number += 1
                print(str(shop_number) + "、" + str(shop))

        except:
            print("------------------\n请求过快，休息5秒！！！\n------------------")
            time.sleep(5)

            # 超过5次获取失败则是号被封了，需等下次恢复~
            if fail_num == 5:
                return shops_list

            continue

        page += 1
        time.sleep(random.randint(1, 8))

    return shops_list


# 从pc端网址，获取所有店铺评论信息并保存
def get_comments(shop, number):
    global comment_number

    page = 1

    comments_list = []

    fail_num = 0
    while True:
        print(str(number) + '、正在获取店铺 ' + str(shop['id'])+ ' (' + str(shop['name']) + ') 第' + str(page) + '页评论：')

        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            #'Cookie': 'uuid=38314cfb231e4bae92a1.1616510460.1.0.0; _lxsdk_cuid=1785f88293ac8-01081aada60609-57442618-144000-1785f88293a2e; mtcdn=K; userTicket=IzLfYYFURpSASVtmoQPspAMQwnQrSUiOrnrSQGwC; lsu=; IJSESSIONID=node0ym3w4jht3jzdk433keuc0f8v21172912; iuuid=BBCD032121B47E9011B614A417D2542E9FC2295BA15D433DD5A4530955DE54E6; webp=1; _lxsdk=BBCD032121B47E9011B614A417D2542E9FC2295BA15D433DD5A4530955DE54E6; __utmc=74597006; __utmz=74597006.1616578855.1.1.utmcsr=link.csdn.net|utmccn=(referral)|utmcmd=referral|utmcct=/; ci3=1; _lx_utm=utm_source%3Dlink.csdn.net%26utm_medium%3Dreferral%26utm_content%3D%252F; _hc.v=4af2f92a-0daa-68cc-2adf-a9fc8875e576.1616579481; ci=42; cityname=%E8%A5%BF%E5%AE%89; a2h=4; rvct=42%2C20%2C1; backurl=http://i.meituan.com/poi/1070552919/feedbacks; token=JqDlE8L7kpgG4fbEQG56-qgaZmwAAAAAJg0AAASXI6Hu1M5u-wIJu0WQQ0CofDq1HVI0y0sx6SP3YTswiHbjcdChET7JhFc5Eg8vvQ; mt_c_token=JqDlE8L7kpgG4fbEQG56-qgaZmwAAAAAJg0AAASXI6Hu1M5u-wIJu0WQQ0CofDq1HVI0y0sx6SP3YTswiHbjcdChET7JhFc5Eg8vvQ; oops=JqDlE8L7kpgG4fbEQG56-qgaZmwAAAAAJg0AAASXI6Hu1M5u-wIJu0WQQ0CofDq1HVI0y0sx6SP3YTswiHbjcdChET7JhFc5Eg8vvQ; userId=2562897915; isid=87EF669CCDF08E10542F7E11F66AFBBE; logintype=normal; __utma=74597006.188086389.1616578855.1616605851.1616647436.5; i_extend=H__a100173__b5; latlng=31.798445,117.20522,1616647443713; lt=Yp7sPkndlPS_AUCr3MTiNlgLjMoAAAAAJg0AAMW_Y6eOzFwhpAvZC_uZVeEQQ-yI6rOv_jcTkE2X6p_wexmflVR4gcup5ANelgP0PA; u=2562897915; n=%E4%B8%8D%E5%96%9C%E6%AC%A2%E5%A4%A7%E6%B5%B7%E7%9A%84%E9%AD%9A; token2=Yp7sPkndlPS_AUCr3MTiNlgLjMoAAAAAJg0AAMW_Y6eOzFwhpAvZC_uZVeEQQ-yI6rOv_jcTkE2X6p_wexmflVR4gcup5ANelgP0PA; unc=%E4%B8%8D%E5%96%9C%E6%AC%A2%E5%A4%A7%E6%B5%B7%E7%9A%84%E9%AD%9A; firstTime=1616674711457; _lxsdk_s=178694e2cf8-4a5-346-3a%7C%7C5',
            'Host': 'www.meituan.com',
            'Pragma': 'no-cache',
            # 'Referer': 'https://www.meituan.com/jiankangliren/' + str(shop['id']) + '/',
            # 'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            # 'sec-ch-ua-mobile': '?0',
            # 'Sec-Fetch-Dest': 'empty',
            # 'Sec-Fetch-Mode': 'cors',
            # 'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/539.36 (KHTML, like Gecko) Chrome/89.0.3689.90 Safari/537.26',
        }
        parameters = {
            'id': shop['id'],
            'offset': 10 * (page - 1),
            'pageSize': 10,
            'mode': 0,
            'starRange': '',
            'userId': '',
            'sortType': 1,
        }
        url = 'https://www.meituan.com/ptapi/poi/getcomment?id=' + str(shop['id']) + '&offset=' + str(10 * (page - 1)) + \
              '&pageSize=10&mode=0&starRange=&userId=&sortType=1'

        dumpJson = json.dumps(parameters)

        try:
            response = requests.get(url, data=dumpJson, headers=headers, timeout=10).text

            datas = json.loads(response)

            # 获取完成
            if datas['comments'] == None:
                print('====================================================================\n 店铺：' + str(shop['name']) +
                      '(' + str(shop['id']) + '）所有评论获取完成！！！\n'
                                              '====================================================================\n')
                break

            for data in datas['comments']:
                comment = {
                    'userName': data['userName'],  # 用户名
                    'menu': data['menu'],  # 项目
                    'score': data['star'] / 10,  # 评分
                    'content': data['comment'],  # 评论内容
                    'reply': data['merchantComment'],  # 商家回复
                    'zanCnt': data['zanCnt'],  # 点赞数
                    'readCnt': data['readCnt'],  # 浏览量
                }

                comments_list.append(comment)
                comment_number += 1
            fail_num = 0

        except:
            fail_num += 1
            if fail_num >= 5:
                print("店铺：" + str(shop['name']) + '(' + str(shop['id']) + '）评论获取失败！ 进度：' + str(page - 1) + '页')
                break

        print(comments_list)
        page += 1

        print('|休息1~5s|')
        time.sleep(random.randint(0, 1))


    df = pd.DataFrame(comments_list)
    df.rename(
        columns={
            'userName': '用户名',
            'menu': '项目',
            'score': '评分',
            'content': '评论内容',
            'reply': '商家回复',
            'zanCnt': '点赞数',
            'readCnt': '浏览量',
        },
        inplace=True
    )

    # 保存文件时去除文件名中的非法字符
    illegal_pattern = re.compile('[/\\\:*?\"<>|]')
    shop_name = re.sub(illegal_pattern, ' ', str(shop['name']))

    save_path = r'information/comments/' + str(shop_name) + '.xlsx'
    df.to_excel(save_path, index=False)  # 保存为xlsx文件（Excel文件），行索引去除
    print("==================================\n商品" + str(shop['id']) + "评论保存成功\n==================================\n")

    time.sleep(random.randint(0, 2))


# 从移动端网址，获取所有店铺评论信息并保存
def get_comments_from_mobile(shop, num):
    global comment_number

    page = 1

    comments_list = []

    while True:
        print(str(num) + '、正在获取店铺 ' + str(shop['id']) + ' (' + str(shop['name']) + ') 第' + str(page) + '页评论：')

        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': '__mta=189226900.1616578855150.1616592713525.1616592716978.20; __mta=189226900.1616578855150.1616592539164.1616592566564.16; uuid=38314cfb231e4bae92a1.1616510460.1.0.0; _lxsdk_cuid=1785f88293ac8-01081aada60609-57442618-144000-1785f88293a2e; mtcdn=K; userTicket=IzLfYYFURpSASVtmoQPspAMQwnQrSUiOrnrSQGwC; lsu=; JSESSIONID=node0ym3w4jht3jzdk433keuc0f8v21172912.node0; IJSESSIONID=node0ym3w4jht3jzdk433keuc0f8v21172912; iuuid=BBCD032121B47E9011B614A417D2542E9FC2295BA15D433DD5A4530955DE54E6; webp=1; _lxsdk=BBCD032121B47E9011B614A417D2542E9FC2295BA15D433DD5A4530955DE54E6; __utmc=74597006; __utmz=74597006.1616578855.1.1.utmcsr=link.csdn.net|utmccn=(referral)|utmcmd=referral|utmcct=/; ci3=1; _lx_utm=utm_source%3Dlink.csdn.net%26utm_medium%3Dreferral%26utm_content%3D%252F; _hc.v=4af2f92a-0daa-68cc-2adf-a9fc8875e576.1616579481; ci=42; cityname=%E8%A5%BF%E5%AE%89; a2h=4; __mta=189226900.1616578855150.1616579039840.1616581458888.7; rvct=42%2C20%2C1; lt=KaKoeVhJcIUGGB81r_1lC0Pi7EsAAAAAJg0AAD7lUunA5AgrbDOEGVemHcaDbLM_S3IWUb3TvSQqIqrZbE4FtF1QKLNBREPSG6_2mQ; u=2562897915; n=%E4%B8%8D%E5%96%9C%E6%AC%A2%E5%A4%A7%E6%B5%B7%E7%9A%84%E9%AD%9A; token2=KaKoeVhJcIUGGB81r_1lC0Pi7EsAAAAAJg0AAD7lUunA5AgrbDOEGVemHcaDbLM_S3IWUb3TvSQqIqrZbE4FtF1QKLNBREPSG6_2mQ; unc=%E4%B8%8D%E5%96%9C%E6%AC%A2%E5%A4%A7%E6%B5%B7%E7%9A%84%E9%AD%9A; isid=8B57D929984CFF9D1D38A35A3445F74A; oops=KaKoeVhJcIUGGB81r_1lC0Pi7EsAAAAAJg0AAD7lUunA5AgrbDOEGVemHcaDbLM_S3IWUb3TvSQqIqrZbE4FtF1QKLNBREPSG6_2mQ; mt_c_token=KaKoeVhJcIUGGB81r_1lC0Pi7EsAAAAAJg0AAD7lUunA5AgrbDOEGVemHcaDbLM_S3IWUb3TvSQqIqrZbE4FtF1QKLNBREPSG6_2mQ; logintype=normal; __utma=74597006.188086389.1616578855.1616578855.1616592529.2; latlng=31.798445,117.20522,1616592535284; i_extend=E148024476249901906254452964925707816757_v5498859325483873764Gimthomepagecategory122H__a100016__b2; firstTime=1616593057454; _lxsdk_s=1786445f21a-546-e01-823%7C%7C34; __utmb=74597006.18.9.1616593313101',
            'Host': 'i.meituan.com',
            'Referer': 'http://i.meituan.com/poi/' + str(shop['id']) + '/feedbacks',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        url = 'http://i.meituan.com/poi/' + str(shop['id']) + '/feedbacks/page_' + str(page)

        html = requests.get(url, headers=headers).text
        print(html)

        soup = BeautifulSoup(html, 'lxml')
        dd_list = soup.select('.dd-padding')

        if len(dd_list) == 0 or dd_list == None:
            print('======================' + str(shop['id']) + ' (' + str(shop['name']) + ') 评论获取完毕======================\n\n')
            break

        for dd in dd_list:
            name = dd.select('.user-wrapper')[0].select('.username')[0].text
            comment_time = dd.select('.user-wrapper')[0].select('.time')[0].text
            score = len(dd.select('.user-wrapper')[0].select('.star_full'))
            content = dd.select('.comment')[0].select('p')[0].text
            reply = ''
            try:
                reply = dd.select('.block-reply')[0].select('p')[0].text
            except:
                pass

            comment = {
                'userName': name,  # 用户名
                'score': score,  # 评分
                'content': content.strip(),  # 评论内容
                'reply': reply.strip(),  # 商家回复
                'time': comment_time,  # 评论时间
            }

            print(comment)
            comments_list.append(comment)
            comment_number += 1

        print(str(page) + '页')
        print('--------------------------')
        page += 1
        time.sleep(random.randint(2, 10))

    # 爬取完毕保存结果
    df = pd.DataFrame(comments_list)
    df.rename(
        columns={
            'userName': '用户名',
            'score': '评分',
            'content': '评论内容',
            'reply': '商家回复',
            'time': '评论时间',
        },
        inplace=True
    )

    # 保存文件时去除文件名中的非法字符
    illegal_pattern = re.compile('[/\\\:*?\"<>|]')
    shop_name = re.sub(illegal_pattern, ' ', str(shop['name']))

    save_path = r'information/comments/' + str(shop_name) + '.xlsx'
    df.to_excel(save_path, index=False)  # 保存为xlsx文件（Excel文件），行索引去除
    print("==================================\n商品" + str(shop['id']) + "评论保存成功\n==================================\n")

    time.sleep(random.randint(5, 10))



# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # # 在项目路径下建立存储评论的文件夹
    # if not os.path.exists(r'information/comments'):
    #     os.mkdir(r'information')
    #     os.mkdir(r'information/comments')
    #     print('当前路径下创建information/comments文件夹成功！')
    # else:
    #     print('当前路径下已存在information/comments文件夹！')
    #
    #
    # # # 获取所有店铺信息
    # # shops_list = get_shops()
    # #
    # # df = pd.DataFrame(shops_list)
    # # df.rename(
    # #     columns={
    # #         'id': 'id',
    # #         'name': '门店名称',
    # #         'price': '人均价格￥',
    # #         'score': '评分',
    # #         'commentNum': '评论数',
    # #         'tag': '门店标签',
    # #         'address': '门店地址',
    # #         'url': '链接',
    # #     },
    # #     inplace=True
    # # )
    # #
    # save_path = r'information/店铺.xlsx'
    # # df.to_excel(save_path, index=False)  # 保存为xlsx文件（Excel文件），行索引去除
    # # print("~店铺信息保存成功~")
    #
    # # 读取文档
    # sheet = pd.read_excel(save_path)
    # sheet.rename(columns={
    #     'id': 'id',
    #     '门店名称': 'name',
    #     '人均价格￥': 'price',
    #     '评分': 'score',
    #     '评论数': 'commentNum',
    #     '门店标签': 'tag',
    #     '门店地址': 'address',
    #     '链接': 'url',
    # }, inplace=True)
    # shops_list = sheet.to_dict('records')  # 按照每行为一个字典对象，转化为字典列表
    #
    #
    # # 开始遍历各店铺的评论
    # for shop in shops_list:
    #     order = shops_list.index(shop) + 1  # 线程序号
    #
    #     if order < 900 or shop['commentNum'] <= 50:
    #         continue
    #
    #     # try:
    #     speed = get_comments(shop, order)
    #     # except:
    #     #     print('切换移动端网站~~~')
    #     #     try:
    #     #         get_comments_from_mobile(shop, shops_list.index(shop))
    #     #     except:
    #     #         time.sleep(20)
    #     #         continue



    result_list = []
    # 读取路径下的所有文件保存至列表中
    files = os.listdir(r'information/comments/')
    for file in files:
        save = str(file)
        sheet = pd.read_excel('information/comments/' + save)
        comments_list = sheet.to_dict('records')
        result_list += comments_list

    df = pd.DataFrame(result_list)
    df.to_excel(r'information/评论汇总.xlsx', index=False)


    #统计时间与数量
    endtime = time.time()  # 获取现在的时间（程序结束时间）
    print('==============================================================\n')
    print('店铺数目共计：' + str(shop_number) + '个\n评论数目共计：' + str(comment_number) + '个\n')
    print('==============================================================\n')
    print('本次爬取耗时：' + str(endtime - starttime) + '秒')
