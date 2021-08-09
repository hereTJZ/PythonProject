import os
import random
import time
import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import parsel
import openpyxl
import lxml
import xlsxwriter

start_time = time.time()


# 获取免费ip代理构建ip池
def get_proxy_list():
    print("~开始获取代理ip~")

    proxy_list = []

    for page in range(1, 10):
        time.sleep(0.3)
        print('正在获取第' + str(page) + '页...')

        url = 'http://www.ip3366.net/?stype=1&page=' + str(page)
        headers = {
            'Referer': 'http://www.ip3366.net/?stype=1&page=' + str(page - 1),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
        }

        response = requests.get(url=url, headers=headers).text  # str类型数据

        # 解析数据
        selector = parsel.Selector(response)  # 转换数据类型，初始化parsel对象
        trs = selector.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr')  # 参考xpath与法规则，开头的/表示根节点

        for tr in trs:
            # 获取ip值和对应端口
            ip_num = tr.xpath('./td[1]/text()').get()  # .表示当前节点
            ip_port = tr.xpath('./td[2]/text()').get()

            ip_proxy = ip_num + ':' + ip_port

            # 代理ip的正确结构
            proxy_dict = {
                'http': 'http://' + ip_proxy,
                'https': 'https://' + ip_proxy
            }

            # 验证该代理ip可用性
            print('成功获取ip:' + str(proxy_dict) + '。 开始验证')
            try:
                response = requests.get(url='https://www.baidu.com', proxies=proxy_dict, timeout=5)
                if response.status_code == 200:
                    proxy_list.append(proxy_dict)
                    print('验证成功，该ip可以使用！！！')
                else:
                    print('status_code：' + str(response.status_code))
            except:
                print('验证失败，该ip不可使用！')
                continue

            print('保存成功：', proxy_dict)

    return proxy_list


# 提取字符串中的数字（评论数）
def extract_number(string):
    iterator = filter(str.isdigit, string)  # 分离字符串中的数字，python3之后的filter()返回的结果是个迭代器
    # print(iterator)  # 结果为<filter object at 0x000002055B11E910>
    digit_list = list(iterator)  # 需要通过list()转换成列表

    result_number = 0
    for i in range(len(digit_list)):
        result_number += int(digit_list[-i - 1]) * pow(10, i)

    return result_number


# 获取满足需求的酒店id列表
def get_hotel_list():
    # 用于存放满足需求的酒店id
    hotel_list = []

    index = 1  # 页数

    while True:
        print('~~获取第' + str(index) + '页酒店~~')

        url = 'https://m.ctrip.com/webapp/hotel/j/hotellistbody?pageid=212093&' \
              'key=fe5%7B%262k%C2%82%C2%808%3As.%3D%3FI35exB%7FrQd999%3AOI%4011380uE~dda421%3FK0f06eebt1204983d&' \
              'huk=Hq4wUtW3qeq1E9QrtYhXYatEzYtXe5FEsOjFdWNYFsrz1wdoItGj1Y0sRdnwpNv6Ny8Ys5j5BiplvAZwBYS0Y1OIgcyO9jnmv04JF9YTQjtMy4YkGvLbIFnYgQwHSIzheqMipQYoY1Yhcvdlel1Y8AiAhY6Y7YLSEStKLNwTPidARBajGrTGYNqJUFylrFlY3SWQ0vOgx4XetkY0pxMTxNtYAciTfwOLjz6EpkJ0BW5kjprk8J1Diotwnfv4pRZ7jQ7Yz0j3rZDyQHiOQwflRQhE6ojLtxf1xkTEGBE0MEs1WGoeAbwPBEF0jNle3Pi0nYFLrF7ePSedgxUPiaAintxhbWS1jaTeg9wlTKHtwntilBRpdjdfeBdEh9yaovA6ipdEOXyDovssK6dEMUK49wNZiUkRQzjarqaYtAJd4yMr10j3SecdjD3K53jN7wF7xB6xpAxzBxglEA1EzMEaHWbPegTwTtEgsjXmeFUisDYk5rOZEBAylGvUoidqEHDypzvXXK8OW09E1Uj4HeLdx5NjkrZhEPdWbHezAjp1YS6jhPxtcxf4xM9xM8ESAEfZEbkWcfeHpwdcEXOjpUeDUih5YZfr1Mem8e3NY6cE1BwocWc9i66KP6EgPEqDEmQWXLeFqwtDENZjPfezni6HYFmrODeSAe4TEUTYmLEBnwgoW7siDY5beSByNhi53iG0j6YHUwqNEbhY5fwOnEaSJXcY16wDYQsRd4wGTRLDY48jB6jAMyo8Y1QRL1wzcvtSEbBy6YznKU5iFBwFUi5kj3Fi79y5OY86JmNydfwg3JSPE1pvdgwP6iHYabRbawthRd0YgoyP3JUqyDnYAaj6dYFqY0ty3XjdYF8jPgwn3vNkjoY3OR4gJlFiGUw9SeaFj6MwUmE9YTlR57JLBiPLwM7e4NjOow43EaYPzR0swh7R0lYtZj1FjFzwD9vcgjGmwkSyz1EtT'

        payloadheader = {
            'authority': 'm.ctrip.com',
            'method': 'POST',
            'path': '/webapp/hotel/j/hotellistbody?pageid=212093&key=fe5%7B%262k%C2%82%C2%808%3As.%3D%3FI35exB%7FrQd999%3AOI%4011380uE~dda421%3FK0f06eebt1204983d&huk=Hq4wUtW3qeq1E9QrtYhXYatEzYtXe5FEsOjFdWNYFsrz1wdoItGj1Y0sRdnwpNv6Ny8Ys5j5BiplvAZwBYS0Y1OIgcyO9jnmv04JF9YTQjtMy4YkGvLbIFnYgQwHSIzheqMipQYoY1Yhcvdlel1Y8AiAhY6Y7YLSEStKLNwTPidARBajGrTGYNqJUFylrFlY3SWQ0vOgx4XetkY0pxMTxNtYAciTfwOLjz6EpkJ0BW5kjprk8J1Diotwnfv4pRZ7jQ7Yz0j3rZDyQHiOQwflRQhE6ojLtxf1xkTEGBE0MEs1WGoeAbwPBEF0jNle3Pi0nYFLrF7ePSedgxUPiaAintxhbWS1jaTeg9wlTKHtwntilBRpdjdfeBdEh9yaovA6ipdEOXyDovssK6dEMUK49wNZiUkRQzjarqaYtAJd4yMr10j3SecdjD3K53jN7wF7xB6xpAxzBxglEA1EzMEaHWbPegTwTtEgsjXmeFUisDYk5rOZEBAylGvUoidqEHDypzvXXK8OW09E1Uj4HeLdx5NjkrZhEPdWbHezAjp1YS6jhPxtcxf4xM9xM8ESAEfZEbkWcfeHpwdcEXOjpUeDUih5YZfr1Mem8e3NY6cE1BwocWc9i66KP6EgPEqDEmQWXLeFqwtDENZjPfezni6HYFmrODeSAe4TEUTYmLEBnwgoW7siDY5beSByNhi53iG0j6YHUwqNEbhY5fwOnEaSJXcY16wDYQsRd4wGTRLDY48jB6jAMyo8Y1QRL1wzcvtSEbBy6YznKU5iFBwFUi5kj3Fi79y5OY86JmNydfwg3JSPE1pvdgwP6iHYabRbawthRd0YgoyP3JUqyDnYAaj6dYFqY0ty3XjdYF8jPgwn3vNkjoY3OR4gJlFiGUw9SeaFj6MwUmE9YTlR57JLBiPLwM7e4NjOow43EaYPzR0swh7R0lYtZj1FjFzwD9vcgjGmwkSyz1EtT',
            'scheme': 'https',
            'accept': 'text/html',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/json',
            'cookie': 'HLDUUID=c315754391134fa58ab8b15d7ab3909a; supportwebp=true; '
                      'list_hotel_price=%7B%22traceid%22%3A%22100004883-5bb9f571-cb58-4639-bfca-d6fb79fb4869%22%2C%22pageid'
                      '%22%3A%22212093%22%2C%22searchcandidate%22%3A%7B%22person%22%3A0%2C%22bedtype%22%3A%22%22%2C'
                      '%22breakfast%22%3A-1%2C%22childs%22%3A%5B%5D%2C%22segmentationno%22%3A0%2C%22showtype%22%3A0%7D%2C'
                      '%22timestamp%22%3A1612886922910%2C%22minpriceroom%22%3A%7B%22roomid%22%3A948794102%2C%22isshadow%22'
                      '%3A0%2C%22shadowId%22%3A0%2C%22avgprice%22%3A380%2C%22currency%22%3A%22RMB%22%2C%22iscanreserve%22%3A1'
                      '%2C%22isusedcoupon%22%3A-1%2C%22isusedcashback%22%3A1%2C%22cashbackamount%22%3A0%2C%22couponamount%22'
                      '%3A0%2C%22reductionamount%22%3A0%2C%22taxfee%22%3A0%7D%2C%22ttype%22%3A0%2C%22icp%22%3A0%2C%22ipd%22'
                      '%3A0%2C%22isopenpricetolerate%22%3A1%2C%22passData%22%3A%7B%22minPriceDetailInfo%22%3A%22%22%7D%7D; '
                      'JSESSIONID=791D9DE21698EC8E79CE1AD7514662E3; _abtest_userid=58961c5b-4b60-4fff-a045-6d602018427b; '
                      'ibulanguage=CN; ibulocale=zh_cn; cookiePricesDisplayed=CNY; _RSG=gaKkrg5ohL53qEtOd.TL39; '
                      '_RGUID=556bc85a-b5b9-492a-90d5-77e9d8dced03; _RDG=283a2b7d8f417c230f00a9975ec13b2324; '
                      '_ga=GA1.2.382965301.1612757285; '
                      'Session=smartlinkcode=U130026&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=; '
                      'Union=AllianceID=4897&SID=130026&OUID=&createtime=1612757285&Expires=1613362085004; '
                      'MKT_CKID=1612757285048.fyywi.uime; MKT_Pagesource=PC; _RF1=183.251.166.193; intl_ht1=h4=10_13666203; '
                      'appFloatCnt=8; librauuid=h3ToVo7nb7TDC96Q; nfes_isSupportWebP=1; '
                      'login_uid=C808DA0DC20EACD88608B05955D94243; login_type=0; '
                      'cticket=571810BF68E171EB3B1F407CB0B17CE7EDB7D1D6BE35A64B4CBF15F791FDF311; '
                      'AHeadUserInfo=VipGrade=10&VipGradeName=%BB%C6%BD%F0%B9%F3%B1%F6&UserName=&NoReadMessageCount=0; '
                      'ticket_ctrip=bJ9RlCHVwlu1ZjyusRi+ypZ7X2r4+yojUWFUVc40PdXWjftDd5UQJy2aVKC3'
                      '/gpLe8bcuRIa2572zuM6CpUyNDU4YcBlQfHT4U+4indVEdsNQSkn'
                      '/LNY7JDVQkJPoI0XlUC9HznKPs8cORrZfxAb1TBOnUe6SFWeqtm8SditlnpSpR0/0YALw/QCMA2v/khcZulL561YvQJRdVM0LgM'
                      '/GZJOnEC03+GoDBdR7P5Um9XYV63v7gOiilmk+UpLv0BqRGMf/3IybbFWZMgeXVjryOj6fh90qspbKENY2THvOFE=; '
                      'DUID=u=8E5C75751E4D3BED104954A9C91D825A&v=0; IsNonUser=F; UUID=4FE3F7463F294554B056A254B05EB860; '
                      'IsPersonalizedLogin=F; _uetsid=93f5e7a06aec11ebb10f6161fcf729f3; '
                      '_uetvid=78689df069c311eb8fae53cfefd1fd7c; MKT_CKID_LMT=1612884990515; '
                      '__zpspc=9.3.1612884990.1612884990.1%232%7Cwww.baidu.com%7C%7C%7C%7C%23; '
                      '_gid=GA1.2.1916656156.1612884991; '
                      '_jzqco=%7C%7C%7C%7C1612884990749%7C1.752738746.1612757285061.1612791879747.1612884990512.1612791879747'
                      '.1612884990512.0.0.0.10.10; hotelhst=1164390341; GUID=09031078311554840816; _bfs=1.5; '
                      '_bfi=p1%3D153002%26p2%3D153002%26v1%3D73%26v2%3D70; '
                      '_bfa=1.1612757282278.opkxn.1.1612799400937.1612886987018.5.77.212093',
            'origin': 'https://m.ctrip.com',
            'referer': "https://m.ctrip.com/webapp/hotel/xi'an10?ulat=0&ulon=0",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
            'x-ctrip-hotel-firend': '----',
            'x-requested-with': 'XMLHttpRequest'

        }

        payloadParam = {
            'abMaps': {},
            'adultCounts': 0,
            'business': 'false',
            # 'checkinDate': "20210210",
            # 'checkoutDate': "20210211",
            'cityID': 10,  # 西安
            'controlBitMap': 1,
            'costPerformanceHigh': 'false',
            'districtID': 0,
            'domesticHotelList': "domesticHotelList",
            'enableAdHotel': 'true',
            'filterItemList': ["brand-110|hotbrand||如家|@kjbrand@brand", "brand-48|hotbrand||汉庭|@kjbrand@brand",
                               "brand-1638|||7天|@kjbrand@brand", "brand-1659|||锦江之星|@kjbrand@brand",
                               "brand-436|||尚客优|@kjbrand@brand", "brand-360|||都市118|@allbrand@brand"],
            'hiddenHotelIDList': [],
            'hiddenHotelIdListStr': "",
            'highestPrice': 0,
            'hotelIdList': [],
            'keyword': "",
            'keywordText': "",
            'locationItemList': [],
            'lowestPrice': 0,
            'multipleHotel': 'false',
            'needLastPageRecommend': 'false',
            'notTopSet': 'false',
            'optionalMap': {'controlBitMapSwitch': "1"},
            'orderItem': "sort-0|1",
            'oversea': 'false',
            'overseaHotelList': "overseaHotelList",
            'pageIndex': 1,
            'pageSize': 10,
            'preCount': 0,
            'preHotelIds': "",
            'relaxation': 'false',
            'roomQuantity': 0,
            'searchByExposedHotSearchKeyword': 'false',
            'searchByExposedZone': 'false',
            'sessionId': "d0375b63-85c9-48a4-a162-cc20f47ef629",
            'showCheckinDate': "02-25",
            'showCheckoutDate': "02-26",
            'showXcfBanner': 'false',
            'starItemList': [],
            'topSet': 'true',
            'topSetHotelList': [],
            'userCityId': 0,
            'userLatitude': 0,
            'userLocationSearch': 'false',
            'userLongitude': 0,
            'userSelectSort': 0,
            # 'validCheckinDate': "20210210"
        }

        # 获取的酒店列表页数
        payloadParam['pageIndex'] = index

        # 将字典类型数据转换为json
        dumpJson = json.dumps(payloadParam)

        html = requests.post(url, data=dumpJson, headers=payloadheader).text
        soup = BeautifulSoup(html, "lxml")

        # <a class="c-be js_a_seo" href="/html5/hotel/hoteldetail/dianping/2152165.html">119条点评</a>
        hotelid_div_list = soup.select('.js_single_hotel')  # soup的选择器select返回的是所有tag类型元素的列表

        # 无结果时酒店列表遍历结束
        if len(hotelid_div_list) == 0:
            break

        for div in hotelid_div_list:
            comment_a_tag = div.find(class_='c-be')  # 找到tag element中class属性值为c-be的子tag

            # 可能存在无评论的情况
            try:
                comment_number = extract_number(comment_a_tag.text)
                if comment_number >= 1000:
                    # 获取酒店评分等数据
                    point = get_overall_evaluation(div['data-id'])

                    hotel = {
                        'id': div['data-id'],
                        'name': div.find(class_='js_a_seo')['title'],
                        'overallPoint': point['overallPoint'],  # 整体评分
                        'recommendRate': point['recommendRate'],  # 推荐度
                        'healthPoint': point['healthPoint'],  # 卫生评分
                        'environmentPoint': point['environmentPoint'],  # 环境评分
                        'servicePoint': point['servicePoint'],  # 服务评分
                        'facilityPoint': point['facilityPoint'],  # 设施评分
                        'commentNum': comment_number  # 评论数
                    }

                    hotel_list.append(hotel)
                    print(str(hotel_list.index(hotel) + 1) + '、获取酒店：' + str(hotel['id']) + ' ' + hotel['name'])
            except:
                print('遇到无评论酒店，跳过~')
                continue

        index += 1

    print('\n成功获取' + str(len(hotel_list)) + '个满足需求的酒店id：' + str(hotel_list))
    return hotel_list


# 获取整体评价
def get_overall_evaluation(id):
    print('正在获取酒店：' + str(id) + ' 的整体评价')

    url = 'https://m.ctrip.com/html5/hotel/hoteldetail/dianping/' + str(id) + '.html'

    # 从原网页html的head标签中可以看出是使用utf-8编码的，所以内容解码也需使用utf-8
    html = requests.get(url).content.decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    evaluation_div = soup.find(class_='hotel-dp-value')

    # 获取整体评分
    overall_score = evaluation_div.find('span').text

    other_score_tags = evaluation_div.select('em')
    other_scores = []
    for i in range(len(other_score_tags)):
        other_scores.append(other_score_tags[i].text)

    result = {
        'overallPoint': overall_score[0:3],  # 整体评分
        'recommendRate': other_scores[0][0:3],  # 推荐度
        'healthPoint': other_scores[1][3:6],  # 卫生评分
        'environmentPoint': other_scores[2][3:6],  # 环境评分
        'servicePoint': other_scores[3][3:6],  # 服务评分
        'facilityPoint': other_scores[4][3:6]  # 设施评分
    }

    return result


# 获取对应格式的店家回复
def get_feedback_content(feedbackList):
    if len(feedbackList) == 0:
        return '店家未回复'

    result = ''
    try:
        for c in feedbackList:
            result += str(feedbackList.index(c) + 1) + '.' + c['title'] + '：' + c['content'] + '\n'
        return result
    except Exception as e:
        print('！！获取店家回复失败！！')


# 累计评论数
number = 0

# 获取酒店评分评论信息并保存
def get_hotel_comment(id):
    url = 'https://m.ctrip.com/restapi/soa2/16765/gethotelcomment?&_fxpcqlniredt=09031078311554840816'

    payloadheader = {
        'authority': 'm.ctrip.com',
        'method': 'POST',
        'path': '/restapi/soa2/16765/gethotelcomment?&_fxpcqlniredt=09031078311554840816',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'cookie': '',
        'origin': 'https://m.ctrip.com',
        'referer': "https://m.ctrip.com/html5/hotel/hoteldetail/dianping/52304413.html",
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': ''
    }

    payloadParam = {
        'basicRoomName': "",
        'groupTypeBitMap': 2,
        'head': {
            'auth': "",
            'cid': "09031078311554840816",
            'ctok': "",
            'cver': "1.0",
            'extension': [],
            'lang': "01",
            'sid': "8888",
            'syscode': "09",
            'xsid': ""

        },
        'hotelId': id,
        'needStatisticInfo': 0,
        'order': 0,
        'pageIndex': 1,  # 评论页数
        'pageSize': 10,
        'tagId': 0,
        'travelType': -1
    }

    # 评论列表
    user_comment_list = []

    i = 1
    while True:
        print('~~获取酒店:' + str(id) + ' 第' + str(i) + '页评论~~')

        payloadParam['pageIndex'] = i
        dumpJson = json.dumps(payloadParam)

        response = requests.post(url, data=dumpJson, headers=payloadheader).text
        print(response)
        datas = json.loads(response)  # 将字符串转换为字典（dict）json类型数据

        if len(datas['othersCommentList']) == 0:
            print('==============================获取完成==============================')
            print(' 当前共获取酒店（' + str(id) + '）：' + str(i - 1) + ' 页评论')
            break

        try:
            for j in range(len(datas['othersCommentList'])):
                content = {
                    'userNickName': datas['othersCommentList'][j]['userNickName'],  # 用户名称
                    'roomName': '',  # 房型
                    'travelType': datas['othersCommentList'][j]['travelType'],  # 旅行方式
                    'ratingPoint': datas['othersCommentList'][j]['ratingPoint'],  # 用户评分
                    'commentContent': datas['othersCommentList'][j]['content'],  # 评论内容
                    'imageUrl': '',  # 评论图片
                    'checkInDate': datas['othersCommentList'][j]['checkInDate'],  # 入住时间
                    'postDate': datas['othersCommentList'][j]['postDate'],  # 发表时间
                    'feedback': '',  # 店家回复内容
                    'remarks': ''  # 备注
                }

                # 房型
                try:
                    content['roomName'] = datas['othersCommentList'][j]['baseRoomName']
                except:
                    pass

                # 评论图片
                images_list = []
                for image in datas['othersCommentList'][j]['imageList']:
                    images_list.append(image['bigImage'])
                content['imageUrl'] = '、\n'.join(images_list)

                # 酒店回复
                try:
                    content['feedback'] = get_feedback_content(datas['othersCommentList'][j]['feedbackList'])
                except Exception as e:
                    pass

                # 备注信息
                try:
                    content['remarks'] = datas['othersCommentList'][j]['sourceText']
                except:
                    pass

                print(content)
                user_comment_list.append(content)

            i += 1

            # 每页之间随机休息0~6s
            s = random.randint(0, 0)
            print('该页爬取完成，休息' + str(s) + '秒')
            time.sleep(s)

        except Exception as e:
            print('\n该ip访问受限，正在切换ip。。。')
            time.sleep(10)
            print(' 当前共获取酒店（' + str(id) + '）：' + str(i - 1) + ' 页评论')
            continue

    global number
    number += len(user_comment_list)
    return user_comment_list


# ======开始执行程序======

# 创建存储酒店及评论信息的文件夹
if not os.path.exists('hotel'):
    os.mkdir('hotel')
    print('创建hotel文件夹成功！')
else:
    print('已存在hotel文件夹！')

# 获取满足条件的酒店信息并保存
hotel_list = get_hotel_list()

save_path = 'hotel/酒店列表.xlsx'
df = pd.DataFrame(hotel_list)
# 列重命名
df.rename(columns={
    'id': '酒店id',
    'name': '酒店名称',
    'overallPoint': '整体评分',
    'recommendRate': '推荐度',
    'healthPoint': '卫生评分',
    'environmentPoint': '环境评分',
    'servicePoint': '服务评分',
    'facilityPoint': '设施评分',
    'commentNum': '评论数'
}, inplace=True)
# 保存为Excel文件
df.to_excel(save_path, index=False)
print('\n==========================保存酒店信息成功！==========================')

# 读取酒店信息列表
print('正在读取酒店信息列表...')
df = pd.read_excel('hotel/酒店列表.xlsx')  # df为Dataframe数据
hotel_list = df.to_dict('records')

print('@成功读取酒店列表：' + str(hotel_list))

# 开始遍历列表获取各酒店评论信息
for i in range(0, len(hotel_list)):
    hotel = hotel_list[i]
    print('--------------------' + str(hotel_list.index(hotel)) + '、正在获取酒店' + str(
        hotel['酒店id']) + '的评论--------------------')
    comment_list = get_hotel_comment(hotel['酒店id'])
    print(comment_list)

    df = pd.DataFrame(comment_list)
    df.rename(columns={
        'userNickName': '用户名称',
        'roomName': '房型',
        'travelType': '旅行方式',
        'ratingPoint': '用户评分',
        'commentContent': '评论内容',
        'imageUrl': '评论图片',
        'checkInDate': '入住时间',
        'postDate': '发表时间',
        'feedback': '回复内容',
        'remarks': '备注'
    }, inplace=True)

    save_path = 'hotel/' + hotel['酒店名称'] + '评论信息.xlsx'
    df.to_excel(save_path, engine='xlsxwriter', index=False)

end_time = time.time()
print('共爬取' + str(len(hotel_list)) + '家酒店总计：' + str(number) + '条评论信息！')

# proxy_list = get_proxy_list()
# hotel_id_list = get_hotel_list()
# print(get_hotel_comment(840368, proxy_list))
