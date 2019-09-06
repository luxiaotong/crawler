import requests
from utils.common import random_ua
from utils.common import get_proxies
import time

def do_request(url, method='GET', params={}):
    result = {}
    ua = random_ua()
    headers = {'User-Agent': ua, 'Content-type': 'application/json'}

    print('当前请求的URL:%s'%url)
    print('当前使用的Method:%s'%method)
    print(params)
    print('当前使用的User-Agent:%s'%ua)

    for j in range(5):
        try:
            proxies = get_proxies()
            print('\t第%d次尝试请求, 使用的Proxy:%s'%(j, proxies['http']))
            if method == 'GET':
                result = requests.get(url, headers=headers, proxies=proxies, timeout=5, params=params)
            elif method == 'POST':
                result = requests.post(url,headers=headers, proxies=proxies, timeout=5, data=params)
        except Exception as e:
            print("Error:", e)
            print('休息,休息一下...(5s)')
            time.sleep(5)
            continue

        print('\t返回结果状态码:%d\n' %result.status_code)
        print('休息,休息一下...(5s)')
        time.sleep(5)

        if result.status_code != 200:
            continue

        break

    return result

url = "http://www.dianping.com/"
result = do_request(url, method='GET')
print(result.cookies.keys())
print(result.cookies.get_dict())
