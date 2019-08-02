import requests
import json
from utils.common import random_ua
from utils.common import get_proxies
import time
import pandas as pd

def do_request(url, method='GET', params={}):
    result = {}
    ua = random_ua()
    headers = {'User-Agent': ua, 'Content-type': 'application/json'}

    print('当前请求的URL:%s' %url)
    print('当前使用的Method:%s' %method)
    print('当前传递的参数', params)
    print('当前使用的User-Agent:%s' %ua)

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

url = "https://www.dianping.com/ajax/citylist/getAllDomesticProvince"
result = do_request(url, method='POST')
provinceList = json.loads(result.text)['provinceList']
city_df = pd.DataFrame()
for i in range(len(provinceList)):
    print('省份:%s\t%s' %(provinceList[i]['provinceId'], provinceList[i]['provinceName']))

    provinceId = provinceList[i]['provinceId']
    params = json.dumps({"provinceId":provinceId})
    url = "https://www.dianping.com/ajax/citylist/getDomesticCityByProvince"
    result = do_request(url, method='POST', params=params)

    print(result.text)
    print(json.loads(result.text))
    print(json.loads(result.text)['cityList'])
    cityList = json.loads(result.text)['cityList']
    if len(cityList) == 0: continue

    city_df = city_df.append(pd.DataFrame(cityList))

# Save City
city_df.to_csv('dianping_city.csv')

# Save Province
province_df = pd.DataFrame(provinceList)
province_df.to_csv('dianping_province.csv')

print('Done!')
