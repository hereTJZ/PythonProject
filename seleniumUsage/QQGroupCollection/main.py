from selenium import webdriver
import requests
import jsonpath
import execjs  # pip install PyExecjs


# 打开浏览器 输入网址  点击登录 获取cookie 驱动
def get_cookies():
    driver = webdriver.Chrome()
    driver.get('https://qun.qq.com/manage.html')
    driver.find_element_by_xpath('//*[@id="headerInfo"]/p[1]/a').click()
    input('如果扫码完成, 请按一下Enter')
    cookie_list = driver.get_cookies()
    print(cookie_list)
    cookie = {}
    for i in cookie_list:
        cookie[i['name']] = i['value']
        with open('cookies.txt', 'w', encoding='utf-8')as f:
            f.write(str(cookie))
    driver.quit()
    with open('cookies.txt', 'r', encoding='utf-8')as f:
        cookie = f.read()
    cookie = eval(cookie)
    return cookie


# cookie sy  得到加密的值bkn
def get_bkn(cookie):
    e = cookie['skey']
    with open('gtk.js', encoding='utf-8')as f:
        JsData = f.read()
    js_text = execjs.compile(JsData)
    bkn = js_text.call('getBkn', e)
    return bkn


# 数据采集
def get_numbers(cookie, bkn):
    headers = {
        'authority': 'qun.qq.com',
        'method': 'POST',
        'path': '/cgi-bin/qun_mgr/search_group_members',
        'origin': 'https://qun.qq.com',
        'referer': 'https://qun.qq.com/member.html',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    url = 'https://qun.qq.com/cgi-bin/qun_mgr/search_group_members'

    offset = 21
    # 0,20    21, 41  42, 62   63 83
    max_qqnumber = []
    gc = input('请输入你要查找的QQ群号码:')
    for index, i in enumerate(range(0, 5001, offset)):

        data = {
            'gc': gc,
            'st': i,
            'end': 20 + offset * index,
            'sort': '0',
            'bkn': bkn,
        }
        req = requests.post(url, headers=headers, data=data, cookies=cookie).json()
        qq_numbers = jsonpath.jsonpath(req, '$..uin')
        qq_names = jsonpath.jsonpath(req, '$..nick')
        try:
            max_qqnumber.append(len(qq_numbers))
            for qq_number, qq_name in zip(qq_numbers, qq_names):
                with open(gc + '.txt', 'a', encoding='utf-8')as f:
                    f.write(str(qq_number) + '----' + qq_name + '\n')
                print('共获得成员数: %d' % sum(max_qqnumber))
        except:
            exit()


"""
1
2
3
面包
面包+鸡蛋
面包加两个鸡蛋    3个面+三个鸡蛋
数据采集  0   20
         21   41
         42    62

bkn算的和网页上一样, 那么证明我算对了? 算BKN 用到了什么? 用到了咱们CK里面的值啊.
"""


def go():
    cookie = get_cookies()
    bkn = get_bkn(cookie)
    get_numbers(cookie, bkn)


# 启动程序
go()