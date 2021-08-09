# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import random
import re
import threading
import time
import requests
import json
import pandas as pd
import os
from bs4 import BeautifulSoup  # BeautifulSoup4

starttime = time.time()


def get_name(uid):
    if uid == HM_UID:
        return "H&M"
    elif uid == ZARA_UID:
        return "ZARA"
    elif uid == Durex_UID:
        return 'Durex'
    elif uid == JISSBON_UID:
        return 'Jissbon'


def get_category_name(tag_category):  # tag_category为粉丝分类标签号，其中【时尚博主：26】【娱乐明星：50】【美妆博主：11】【搞笑幽默博主：20】...
    if tag_category == 11:
        return "美妆博主"
    elif tag_category == 12:
        return '体育博主'
    elif tag_category == 15:
        return '婚庆服务博主'
    elif tag_category == 18:
        return '情感两性博主'
    elif tag_category == 19:
        return '财经博主'
    elif tag_category == 20:
        return '搞笑幽默博主'
    elif tag_category == 21:
        return '摄影拍照博主'
    elif tag_category == 24:
        return '教育博主'
    elif tag_category == 25:
        return "旅游出行博主"
    elif tag_category == 26:
        return "时尚博主"
    elif tag_category == 27:
        return "星座命理博主"
    elif tag_category == 28:
        return "母婴育儿博主"
    elif tag_category == 29:
        return "汽车博主"
    elif tag_category == 30:
        return "法律博主"
    elif tag_category == 31:
        return '数码博主'
    elif tag_category == 32:
        return '游戏博主'
    elif tag_category == 33:
        return '电影博主'
    elif tag_category == 34:
        return '电视剧博主'
    elif tag_category == 35:
        return '科学科普博主'
    elif tag_category == 36:
        return '综艺节目博主'
    elif tag_category == 39:
        return '帅哥美女博主'
    elif tag_category == 41:
        return '美食博主'
    elif tag_category == 43:
        return '设计美学博主'
    elif tag_category == 44:
        return '读书作家博主'
    elif tag_category == 45:
        return '运动健身博主'
    elif tag_category == 46:
        return '音乐博主'
    elif tag_category == 48:
        return '公益博主'
    elif tag_category == 50:
        return "娱乐明星"
    elif tag_category == 50:
        return "房地产博主"
    elif tag_category == 55:
        return "家居博主"
    elif tag_category == 60:
        return "时事博主"
    elif tag_category == 61:
        return "历史博主"
    elif tag_category == 10000:
        return "职场博主"
    elif tag_category == 10001:
        return "收藏博主"


def get_fans_id_list(uid, tag_category):  # 这里uid为品牌官博id
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/'
                      '537.36 (KHTML, like Gecko)Chrome/87.0.4280.66Safari/537.36',
        'Referer': 'https://m.weibo.cn/p/index?'
                   'containerid=231051_-_followerstagBigV_-_' + str(uid) + '_-_1042015%3AtagCategory_' + str(
            tag_category) + '&'
                            'luicode=10000011&lfid=231051_-_fans_-_1744769622',

        # 只要Cookie对了即可模拟登录成功
        'Cookie': '_T_WM=35409028016; '
                  'WEIBOCN_FROM=1110006030; '
                  'MLOGIN=1; '
                  'M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D231051_-_fans_-_2049875433%26fid%3D231051_-_followerstagBigV_-_2049875433_-_1042015%253AtagCategory_011%26uicode%3D10000011; '
                  'SUB=_2A25NHfUqDeRhGeBL7FQY8yfFzD-IHXVu4ZtirDV6PUJbktAfLRnVkW1NRs0OTkc3CEp1P3X6ryHcpj16Fkip4qAk; '  # 似乎不会变 
                  'SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFefwHKb6KXmLPoVNcAoUze5JpX5KzhUgL.FoqfS0q4e0.4S0e2dJLoIXnLxKBLBonL12BLxK-L1KqL1-eLxKqLB-BLBK2LxK-LBKBLBKMLxKqLBo-LBoMLxKML1-2L1hBLxK.LB-BL1-2LxK-L1KMLB-qt; '
                  'SSOLoginState=1612285306; '  # 似乎不会变 
                  'SCF=AlMeFNVrkwqgo7Q7IQAibLADj7qXd7uHpKaudqFohWBQIJ0COMKoW9LzmeSLIqkNqUxOITysWGTfrqJBi3DnM4c.; '  # 似乎不会变
                  'ALF=1614877306; '  # 似乎不会变
                  'XSRF-TOKEN=8fb2de; '  # 会变
    }

    base_url = 'https://m.weibo.cn/api/container/getIndex?' \
               'containerid=231051_-_followerstagBigV_-_' + str(uid) + '_-_1042015%3AtagCategory_' + str(
        tag_category) + '&' \
                        'luicode=10000011&' \
                        'lfid=231051_-_fans_-_1744769622&' \
                        'since_id='  # 列表页面id

    fans_id_list = []
    i = 1
    while True:
        response = requests.get(base_url + str(i), headers).text
        datas = json.loads(response)  # 将字符串转换为字典（dict）json类型数据
        if datas['ok'] == 0:
            break

        list_len = len(datas['data']['cards'][0]['card_group'])
        for j in range(list_len):
            fan_id = datas['data']['cards'][0]['card_group'][j]['user']['id']
            # uname = datas['data']['cards'][0]['card_group'][j]['user']['screen_name']
            fans_id_list.append(fan_id)

        print('成功获取' + get_name(uid) + '第' + str(i) + '组' + get_category_name(tag_category) + '粉丝uid')
        print('共计：' + str(len(fans_id_list)) + '个粉丝')
        print(pd.DataFrame(fans_id_list))
        i += 1

    return fans_id_list


def get_fan_info_from_homepage(uid):
    headers = {
        'Referer': 'https://m.weibo.cn/u/' + str(uid),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/87.0.4280.66 Safari/537.36 '
    }

    base_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + str(uid) + '&containerid=100505' + str(uid)

    response = requests.get(base_url, headers).text
    datas = json.loads(response)
    user_info_one = {
        'uid': uid,
        'screen_name': '',
        'description': '',
        'follow_count': int,
        'followers_count': int,
        'gender': '',
        'urank': int,
        'statuses_count': int,
        'mbrank': int,
    }
    if datas['ok'] == 1:
        user_info_one = {
            'uid': uid,
            'screen_name': datas['data']['userInfo']['screen_name'],
            'description': datas['data']['userInfo']['description'],
            'follow_count': datas['data']['userInfo']['follow_count'],
            'followers_count': datas['data']['userInfo']['followers_count'],
            'gender': datas['data']['userInfo']['gender'],
            'urank': datas['data']['userInfo']['urank'],
            'statuses_count': datas['data']['userInfo']['statuses_count'],
            'mbrank': datas['data']['userInfo']['mbrank'],
        }
        if datas['data']['userInfo']['verified']:
            user_info_one['verify_info'] = datas['data']['userInfo']['verified_reason']
        else:
            user_info_one['verify_info'] = '未认证'

    return user_info_one


def get_fan_info_from_basic_info(uid):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'Referer: https://m.weibo.cn/p/index?containerid=230283' + str(uid) + '_-_INFO',
        'X-XSRF-TOKEN': '5791f0',
        'Cookie': '_T_WM=58269110952; '  # 会变 
                  'MLOGIN=1; '
                  'M_WEIBOCN_PARAMS=lfid%3D2302833289336410_-_INFO%26luicode%3D20000174%26fid%3D2302833289336410_-_INFO%26uicode%3D10000011; '  # 会变 
                  'SUB=_2A25NHhBqDeRhGeBL7FQY8yfFzD-IHXVu4LAirDV6PUJbkdANLVnckW1NRs0OTi288dBTezrApu8CqdsGjzbVjHSO; '  # 似乎不会变 
                  'XSRF-TOKEN=5791f0; '  # 会变
                  'WEIBOCN_FROM=1110006030'  # 似乎不会变
    }

    base_url = 'https://m.weibo.cn/api/container/getIndex?containerid=230283' + str(uid) + '_-_INFO'

    response = requests.get(base_url, headers=headers).text

    datas = json.loads(response)

    user_info_two = {
        'register_time': '',
        'birthday': '',
        'location': ''
    }  # 对象中的值可以不用列出，直接 user_info_two = {} 后面引用的时候会直接创建
    if datas['ok'] == 1:
        for i in range(2):
            for j in range(len(datas['data']['cards'][i]['card_group'])):
                try:
                    if datas['data']['cards'][i]['card_group'][j]['item_name'] == "注册时间":
                        user_info_two['register_time'] = datas['data']['cards'][i]['card_group'][j]['item_content']
                        print('获取注册时间：' + user_info_two['register_time'])
                    if datas['data']['cards'][i]['card_group'][j]['item_name'] == "生日":
                        user_info_two['birthday'] = datas['data']['cards'][i]['card_group'][j]['item_content']
                        print('获取生日：' + user_info_two['birthday'])
                    if datas['data']['cards'][i]['card_group'][j]['item_name'] == "所在地":
                        user_info_two['location'] = datas['data']['cards'][i]['card_group'][j]['item_content']
                        print('获取所在地：' + user_info_two['location'])
                except KeyError:
                    pass
    # 遇到‘请求频繁’出错时，程序休眠时间加长
    elif datas['ok'] == 0:
        print('请求过于频繁,歇歇吧~~')
        time.sleep(random.randint(100, 200))

    global fail_num
    if user_info_two['register_time'] != '':
        fail_num = 0
        return user_info_two
    else:
        fail_num += 1
        if fail_num <= 3:
            time.sleep(random.randint(0, 6))  # 查询失败了随机休息0~6秒继续执行
            return get_fan_info_from_basic_info(uid)
        else:
            fail_num = 0
            return user_info_two


fail_num = 0


def get_tag_name(uid):
    url = 'https://weibo.cn/account/privacy/tags/?uid=' + str(uid)
    headers = {
        'Cookie': '_T_WM=58269110952; '
                  'M_WEIBOCN_PARAMS=lfid%3D2302833289336410_-_INFO%26luicode%3D20000174; '
                  'SUB=_2A25NHhBqDeRhGeBL7FQY8yfFzD-IHXVu4LAirDV6PUJbkdANLVnckW1NRs0OTi288dBTezrApu8CqdsGjzbVjHSO; '
                  'MLOGIN=1 '
    }

    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    # print(soup.prettify())  # prettify()是将html标签语言规范化输出
    # print(soup.find_all(text=re.compile('标签')))
    a_list = soup.select('.c a')
    # print(pd.DataFrame(a_list))
    tag_name = ''
    begin = -1
    end = 100
    for a in a_list:
        if a.text == a.find(text=re.compile('资料')):
            begin = a_list.index(a)
        if a.text == a.find(text=re.compile('皮肤')):
            end = a_list.index(a)
        if (begin != -1) and (begin + 2) <= a_list.index(a) < end:
            tag_name += (a.text + '、')

    if tag_name.strip('、') != '':
        return tag_name.strip('、')  # 返回去掉头尾所有的分号
    else:
        return '无'


def gender(string):
    if string == 'm':
        return '男'
    if string == 'f':
        return '女'


def merge_user_info(info_one, info_two):
    user_info = {
        'uid': info_one['uid'],  # uid
        'nickname': info_one['screen_name'],  # 昵称screen_name
        'category': '',  # 类别
        'verify_info': info_one['verify_info'],  # 认证信息verified_reason
        'location': info_two['location'],  # 所在地
        'gender': gender(info_one['gender']),  # 性别
        'birthday': info_two['birthday'],  # 生日
        'description': info_one['description'],  # 个人简介
        'register_time': info_two['register_time'],  # 注册时间
        'tag_name': '',  # 标签
        'urank': info_one['urank'],  # 用户等级
        'mbrank': info_one['mbrank'],  # 会员等级
        'follow_count': info_one['follow_count'],  # 关注数
        'followers_count': info_one['followers_count'],  # 粉丝数
        'statuses_count': info_one['statuses_count'],  # 博客数
    }

    return user_info


number = 0  # 统计粉丝数
def get_user_info(ID, TAG):
    print('@、启动线程：' + get_name(ID) + '(' + str(ID) + ')' + '_' + get_category_name(TAG) + '类粉丝')

    ids_list = get_fans_id_list(ID, TAG)

    lock1.acquire()  # 多个线程会最开始抢这个锁，拿到锁就会处于关锁，执行后面的程序，其他线程执行处于监听状态，等待这个线程开锁，再抢锁
    global number
    number += len(ids_list)
    lock1.release()  # 释放锁

    user_info_list = []
    a = 1

    # 设置文件保存路径并检查文件是否存在且最新状态，是则跳过，否则重新爬取
    save_path = r'fans_info/' + get_name(ID) + '_' + get_category_name(TAG) + '类.xlsx'
    if os.path.exists(save_path):
        sheet = pd.read_excel(save_path)  # 读取列表为Dataframe结构数据
        read_uid = sheet.loc[0]['uid']
        if read_uid == ids_list[0]:
            print(get_name(ID) + '_' + get_category_name(TAG) + '类.xlsx文件已存在且为最新版本')
            return 0

    for uid in ids_list:
        user = merge_user_info(get_fan_info_from_homepage(uid), get_fan_info_from_basic_info(uid))
        user['category'] = get_category_name(TAG)
        user['tag_name'] = get_tag_name(uid)
        user_info_list.append(user)
        print(str(a) + '、' + user['nickname'] + ':' + str(user['uid']) + ' 添加成功!')
        a += 1
        time.sleep(random.randint(1, 3))

    df = pd.DataFrame(user_info_list)
    df.rename(columns={
        'uid': 'uid',
        'nickname': '昵称',
        'category': '类别',
        'verify_info': '微博认证',
        'location': '所在地',
        'gender': '性别',
        'birthday': '生日',
        'description': '个人简介',
        'register_time': '注册时间',
        'tag_name': '标签',
        'urank': '用户等级',
        'mbrank': '会员等级',
        'follow_count': '关注数',
        'followers_count': '粉丝数',
        'statuses_count': '博客数'
    },
        inplace=True)
    # os.getcwd()可以获取当前路径，同理r表示当前路径
    df.to_excel(save_path, index=False)  # 保存为xlsx文件（Excel文件），行索引去除

    print('@结束线程：' + get_name(ID) + '(' + str(ID) + ')' + '_' + get_category_name(TAG) + '类粉丝')
    print('该类粉丝数目共计：' + str(len(ids_list)) + '个\n')


# Press the green button in the gutter to run the script.
HM_UID = 2049875433  # H&M官方账号uid
ZARA_UID = 1744769622  # ZARA官方账号uid
Durex_UID = 1942473263  # 杜蕾斯官方账号uid
JISSBON_UID = 1677892343  # 杰士邦官方账号uid

tags1 = [20, 31, 41]
tags2_1 = [12, 19, 20]
tags2_2 = [25, 26, 31]
tags2_3 = [32, 39, 41]
ids = [Durex_UID, JISSBON_UID]

# 创建存储粉丝信息的文件夹
if not os.path.exists(r'fans_info'):
    os.mkdir(r'fans_info')
    print('当前路径下创建fans_info文件夹成功！')
else:
    print('当前路径下已存在fans_info文件夹！')

lock1 = threading.Lock()  # 线程锁，用于防止多个线程同时修改一个全局变量
threads_list = []

for TAG in tags1:
    t = threading.Thread(target=get_user_info, args=(Durex_UID, TAG))
    t.start()
    threads_list.append(t)
# 阻塞主线程，直至该线程结束，主线程才继续运行
for i in range(len(threads_list)):
    threads_list[i].join()


for TAG in tags2_1:
    t = threading.Thread(target=get_user_info, args=(JISSBON_UID, TAG))
    t.start()
    threads_list.append(t)
# 阻塞主线程，直至该线程结束，主线程才继续运行
for i in range(len(threads_list)):
    threads_list[i].join()

for TAG in tags2_2:
    t = threading.Thread(target=get_user_info, args=(JISSBON_UID, TAG))
    t.start()
    threads_list.append(t)
# 阻塞主线程，直至该线程结束，主线程才继续运行
for i in range(len(threads_list)):
    threads_list[i].join()

for TAG in tags2_3:
    t = threading.Thread(target=get_user_info, args=(JISSBON_UID, TAG))
    t.start()
    threads_list.append(t)
# 阻塞主线程，直至该线程结束，主线程才继续运行
for i in range(len(threads_list)):
    threads_list[i].join()


endtime = time.time()
print('本次累计爬取粉丝数目：' + str(number) + '个\n')
print('本次爬取耗时：' + str(endtime - starttime) + '秒')
