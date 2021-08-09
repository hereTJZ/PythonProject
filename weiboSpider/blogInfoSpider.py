# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
import random
import re
import threading
import time
from abc import ABC
from html.parser import HTMLParser
from sys import stderr
from traceback import print_exc
import requests
import json
import pandas as pd
import os
import openpyxl
import lxml
from bs4 import BeautifulSoup  # BeautifulSoup4


starttime = time.time()  # 获取现在的时间（程序开始时间）


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


def get_fans_list(uid, tag_category):  # 这里uid为品牌官博id
    headers = {

    }

    base_url = 'https://m.weibo.cn/api/container/getIndex?' \
               'containerid=231051_-_followerstagBigV_-_' + str(uid) + '_-_1042015%3AtagCategory_' + str(
        tag_category) + '&' \
                        'luicode=10000011&' \
                        'lfid=231051_-_fans_-_1744769622&' \
                        'since_id='  # 列表页面id

    fans_list = []
    i = 1
    while True:
        response = requests.get(base_url + str(i), headers).text
        datas = json.loads(response)  # 将字符串转换为字典（dict）json类型数据
        if datas['ok'] == 0:
            break
        user = {
            'uid': '',
            'nickname': '',
            'category': ''
        }
        list_len = len(datas['data']['cards'][0]['card_group'])
        for j in range(list_len):
            user = {
                'uid': datas['data']['cards'][0]['card_group'][j]['user']['id'],
                'nickname': datas['data']['cards'][0]['card_group'][j]['user']['screen_name'],
                'category': get_category_name(tag_category)
            }
            print(user)
            fans_list.append(user)

        print('成功获取' + get_name(uid) + '第' + str(i) + '组' + get_category_name(tag_category) + '粉丝信息')
        i += 1

    return fans_list


# 获取博客长文本内容
def get_long_text_conent(blog_id):
    # 博客全文内容在 “https://m.weibo.cn/statuses/extend?id= ”链接下的longTextContent中
    base_url = 'https://m.weibo.cn/statuses/extend?id='
    response = requests.get(base_url + str(blog_id)).text
    datas = json.loads(response)
    if datas['ok'] == 1:
        html_text = datas['data']['longTextContent']
        return parse_html(html_text)
    else:
        return '详情查看链接：' + base_url + str(blog_id)


# 解析位于博客text中的html语言为纯文本内容
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


def get_blogs(user):
    print('正在获取用户：' + str(user['uid']) + '（' + user['nickname'] + '）' + '的博客信息~')

    headers = {
        'Cookie': ''
    }

    base_url = 'https://m.weibo.cn/api/container/getIndex?containerid=230413' + str(user['uid']) + '&page_type=03&page='

    user_blogs_list = []  # 某用户的博客信息列表

    i = 1
    try:
        while True:
            print('正在获取用户：' + str(user['uid']) + '（' + user['nickname'] + '）' + '页数:' + str(i))
            response = requests.get(base_url + str(i)).text  # 页面内容
            datas = json.loads(response)

            # 循环出口1：获取至博客最后一页下一页
            if ('name' in datas['data']['cards'][0]) and (datas['data']['cards'][0]['name'] == '暂无微博'):
                print('该页暂无微博')
                print('用户：' + str(user['uid']) + '（' + user['nickname'] + '）微博内容获取完成！！')
                break

            cards_len = len(datas['data']['cards'])
            first_create_time = datas['data']['cards'][0]['mblog']['created_at']  # 博客列表中第一个博客的发布时间
            last_create_time = datas['data']['cards'][cards_len - 1]['mblog']['created_at']  # 博客列表中最后一个博客的发布时间

            first_time_format = datetime.datetime.strptime(first_create_time, '%a %b %d %H:%M:%S %z %Y')  # 格式化为指定的时间类型
            last_time_format = datetime.datetime.strptime(last_create_time, '%a %b %d %H:%M:%S %z %Y')  # 格式化为指定的时间类型

            # final_first_time = str(first_time_format)[0:19]  # 将时间类型转换成字符串,并且指定字符串长度
            # print(final_first_time)  # 输出

            begin_date_time = first_time_format.date()  # 博客列表中第一个博客的发布日期
            end_date_time = last_time_format.date()  # 博客列表中最后一个博客的发布日期

            begin_date = datetime.date(2021, 1, 1)
            end_date = datetime.date(2021, 1, 31)
            if (end_date_time > end_date) and i != 1:
                i += 1
                print('该页不在需求时间范围内')
                continue

            # 循环出口2：超出需求时间的博客
            if (begin_date_time < begin_date) and i != 1:
                print('需求时间范围内博文获取成功~')
                print('用户：' + str(user['uid']) + '（' + user['nickname'] + '）微博内容获取完成！！')
                break

            for j in range(cards_len):
                blog_info = {
                    'uid': '',  # uid
                    'nickname': '',  # 昵称screen_name
                    'category': '',  # 类别tag_category
                    'blog_id': '',  # 博客id
                    'source': '新浪客户端',  # 来自source
                    'blog_type': 'text',  # 博客类型
                    'content': '',  # 博客内容text
                    'images_url': '无',  # 图片(视频、直播)链接，根据pic_num
                    'blog_url': '',  # 博客页面链接链接scheme
                    'time': '',  # 发布时间created_at
                    'reposts_count': '',  # 转发数reposts_count
                    'comments_count': '',  # 评论数comments_count
                    'attitudes_count': '',  # 点赞数attitudes_count
                    'is_original': True,  # 原创与否
                    'forward_user': '',  # 被转发人
                    'retweet_reason': '',  # 转发理由
                    'original_reposts_count': '',  # 原转发数
                    'original_comments_count': '',  # 原评论数
                    'original_attitudes_count': '',  # 原点赞数
                    'remark_info': ''  # 备注信息
                }

                blog = datas['data']['cards'][j]['mblog']

                blog_info['blog_id'] = blog['id']
                print(str(j + 1) + '、博客id：' + blog_info['blog_id'])

                # 判断博客时间是否在需求时间范围内
                create_time = blog['created_at']
                format_time = datetime.datetime.strptime(create_time, '%a %b %d %H:%M:%S %z %Y')
                if begin_date > format_time.date() or format_time.date() > end_date:
                    print('该博客不在需求时间范围之内')
                    continue

                show_time = str(format_time)[0:19]
                blog_info['time'] = show_time

                blog_info['attitudes_count'] = blog['attitudes_count']
                blog_info['comments_count'] = blog['comments_count']
                blog_info['reposts_count'] = blog['reposts_count']
                blog_info['source'] = blog['source']
                blog_info['blog_url'] = 'https://m.weibo.cn/detail/' + str(blog_info['blog_id'])

                # 查看详细博客文章可能会遇到需要登录或无权限查看的情况，这时直接获取列表中的博文
                try:
                    blog_info['content'] = get_long_text_conent(blog_info['blog_id'])
                except:
                    blog_info['content'] = parse_html(blog['text'])

                # 博客照片、视频或直播链接
                url_list = []
                if blog['pic_num'] != 0:
                    base_images_url = blog['original_pic'][0:29]
                    for k in range(len(blog['pic_ids'])):
                        image_url = base_images_url + blog['pic_ids'][k] + '.jpg'
                        url_list.append(image_url)
                    separator = '、\n'
                    images_url = separator.join(url_list)

                    blog_info['images_url'] = '图片链接：\n' + images_url

                # 转推博客的情况
                if 'retweeted_status' in blog:
                    retweet = blog['retweeted_status']
                    # 转发的微博可能存在无权限查看的问题，要避免该类问题
                    try:
                        blog_info['forward_user'] = retweet['user']['screen_name'] + '（' + str(retweet['user']['id']) + '）'
                        blog_info['original_reposts_count'] = retweet['reposts_count']
                        blog_info['original_comments_count'] = retweet['comments_count']
                        blog_info['original_attitudes_count'] = retweet['attitudes_count']
                    except:
                        blog_info['forward_user'] = '抱歉，由于作者设置，无查看权限'
                        blog_info['original_reposts_count'] = '抱歉，由于作者设置，无查看权限'
                        blog_info['original_comments_count'] = '抱歉，由于作者设置，无查看权限'
                        blog_info['original_attitudes_count'] = '抱歉，由于作者设置，无查看权限'
                    blog_info['is_original'] = False
                    blog_info['retweet_reason'] = blog_info['content']
                    blog_info['blog_type'] = '转推博客'
                # 原创博客情况下
                elif 'page_info' in blog:
                    blog_info['blog_type'] = blog['page_info']['type']
                    # 博客类型为视频或直播的情况下：
                    if blog_info['blog_type'] == 'vedio':
                        blog_info['images_url'] = '视频链接：\n' + blog['page_info']['page_url']
                    elif blog_info['blog_type'] == 'live':
                        blog_info['images_url'] = '直播（回放）链接：\n' + blog['page_info']['page_url']

                # 备注信息，例如置顶博客
                try:
                    if 'title' in blog:
                        blog_info['remark_info'] = blog['title']['text']
                except:
                    pass

                # 为博客添加博主信息
                blog_info['uid'] = user['uid']
                blog_info['nickname'] = user['nickname']
                blog_info['category'] = user['category']

                # 最后添加至某博主的博客列表中
                print(blog_info)
                user_blogs_list.append(blog_info)

            i += 1

    except:
        print(threading.current_thread().getName() + '休息100~200秒')
        time.sleep(random.randint(100, 200))
        return get_blogs(user)

    return user_blogs_list


def gender(string):
    if string == 'm':
        return '男'
    if string == 'f':
        return '女'


# 统计所有博客数
number = 0
def get_blogs_info(Id, tag):
    print('启动线程：' + get_name(Id) + '(' + str(Id) + ')' + '_' + get_category_name(tag) + '类粉丝')

    # 某类粉丝的所有博客信息列表
    blogs_list = []

    # 获取所有某一类别的粉丝
    fans_list = get_fans_list(Id, tag)

    print(pd.DataFrame(fans_list))

    # 获取列表里所有粉丝的博客
    for fan in fans_list:
        print('~~~获取粉丝列表第：' + str(fans_list.index(fan)) + '位粉丝博客信息~~~')
        blogs_list += get_blogs(fan)

    lock1.acquire()
    global number
    number += len(blogs_list)
    print('共计：' + str(len(blogs_list)) + '个博客')
    lock1.release()

    df = pd.DataFrame(blogs_list)
    df.rename(columns={
        'uid': 'uid',  # uid
        'nickname': '昵称',  # 昵称screen_name
        'category': '类别',  # 类别tag_category
        'blog_id': '博客id',  # 博客id
        'source': '博客来自',  # 来自source
        'blog_type': '博客类型',  # 博客类型
        'content': '博客内容',  # 博客内容text
        'images_url': '资源链接',  # 图片(视频、直播)链接，根据pic_num
        'blog_url': '博客链接',  # 博客页面链接链接scheme
        'reposts_count': '转发数',  # 转发数reposts_count
        'comments_count': '评论数',  # 评论数comments_count
        'attitudes_count': '点赞数',  # 点赞数attitudes_count
        'time': '发布时间',  # 发布时间created_at
        'is_original': '是否原创',  # 是否原创
        'retweet_reason': '转发理由',  # 转发理由
        'forward_user': '被转发人',  # 被转发人
        'original_reposts_count': '原转发数',  # 原转发数
        'original_comments_count': '原评论数',  # 原评论数
        'original_attitudes_count': '原点赞数',  # 原点赞数
        'remark_info': '备注'  # 备注信息
        },
        inplace=True
    )

    save_path = r'blogs_info/' + get_name(Id) + '_' + get_category_name(tag) + '类.xlsx'
    df.to_excel(save_path, index=False)  # 保存为xlsx文件（Excel文件），行索引去除

    return number


# Press the green button in the gutter to run the script.

HM_UID = 2049875433  # H&M官方账号uid
ZARA_UID = 1744769622  # ZARA官方账号uid
Durex_UID = 1942473263  # 杜蕾斯官方账号uid
JISSBON_UID = 1677892343  # 杰士邦官方账号uid


tags1_1 = [20]
tags1_2 = [31, 41]

tags2_1 = [12, 19]
tags2_2 = [20]
tags2_3 = [25, 26]
tags2_4 = [31, 32]
tags2_5 = [39, 41]
ids = [Durex_UID, JISSBON_UID]

if not os.path.exists(r'blogs_info'):
    os.mkdir(r'blogs_info')
    print('当前路径下创建blogs_info文件夹成功！')
else:
    print('当前路径下已存在blogs_info文件夹！')


lock1 = threading.Lock()  # 线程锁，用于防止多个线程同时修改一个全局变量
threads_list = []


for TAG in tags2_1:
    t = threading.Thread(target=get_blogs_info, args=(JISSBON_UID, TAG))
    t.start()
    threads_list.append(t)
# 阻塞主线程，直至该线程结束，主线程才继续运行
for i in threads_list:
    i.join()

for TAG in tags2_2:
    t = threading.Thread(target=get_blogs_info, args=(JISSBON_UID, TAG))
    t.start()
    threads_list.append(t)
# 阻塞主线程，直至该线程结束，主线程才继续运行
for i in threads_list:
    i.join()

for TAG in tags2_3:
    t = threading.Thread(target=get_blogs_info, args=(JISSBON_UID, TAG))
    t.start()
    threads_list.append(t)
# 阻塞主线程，直至该线程结束，主线程才继续运行
for i in threads_list:
    i.join()

for TAG in tags2_4:
    t = threading.Thread(target=get_blogs_info, args=(JISSBON_UID, TAG))
    t.start()
    threads_list.append(t)
# 阻塞主线程，直至该线程结束，主线程才继续运行
for i in threads_list:
    i.join()

for TAG in tags2_5:
    t = threading.Thread(target=get_blogs_info, args=(JISSBON_UID, TAG))
    t.start()
    threads_list.append(t)
# 阻塞主线程，直至该线程结束，主线程才继续运行
for i in threads_list:
    i.join()



for TAG in tags1_1:
    t = threading.Thread(target=get_blogs_info, args=(Durex_UID, TAG))
    t.start()
    threads_list.append(t)
# 阻塞主线程，直至该线程结束，主线程才继续运行
for i in threads_list:
    i.join()

for TAG in tags1_2:
    t = threading.Thread(target=get_blogs_info, args=(Durex_UID, TAG))
    t.start()
    threads_list.append(t)
# 阻塞主线程，直至该线程结束，主线程才继续运行
for i in threads_list:
    i.join()

endtime = time.time()  # 获取现在的时间（程序结束时间）
print('所有博客数目共计：' + str(number) + '个\n')
print('本次爬取耗时：' + str(endtime - starttime) + '秒')
