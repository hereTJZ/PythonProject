import requests

# 太阳软件动态ip，每日免费50个，只可以提取一次！！！！
# ip_json = requests.get('http://http.tiqu.alibabaapi.com/getip?num=50&type=2&pack=63941&port=1&lb=1&pb=4&regions=').text
# print(ip_json)
ip_json = {"code": 0, "data": [{"ip": "221.230.174.9", "port": "4353"}, {"ip": "139.212.206.216", "port": "4356"}],
           "msg": "0", "success": True}

for i in range(len(ip_json['data'])):
    proxy_dict = {
        'http': 'http://' + ip_json['data'][i]['ip'] + ':' + ip_json['data'][i]['port'],
        'https': 'https://' + ip_json['data'][i]['ip'] + ':' + ip_json['data'][i]['port']
    }

    # 验证该代理ip可用性
    print('成功获取ip:' + str(proxy_dict) + '。 开始验证')
    try:
        response = requests.get(url='https://www.baidu.com', proxies=proxy_dict, verify=False)  # verify是否验证服务器的SSL证书
        if response.status_code == 200:
            print('验证成功，该ip可以使用！！！')
        else:
            print('status_code：' + str(response.status_code))

        print(response.content.decode('utf-8'))

    except Exception as e:
        print('验证失败，该ip不可使用！')
        print(e)
