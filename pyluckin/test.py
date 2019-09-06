import requests
import json
from utils.common import random_ua
from utils.common import get_proxies
import time
import pandas as pd
from bs4 import BeautifulSoup

def do_request(url, method='GET', params={}):
    result = {}
    ua = random_ua()
    headers = {'User-Agent': ua, 'Content-type': 'application/json'}
    #cookies = {
    #    '_lxsdk_cuid':'16bc0c98a9fc8-0be68b564974c3-37647e05-1fa400-16bc0c98a9fc8',
    #    '_lxsdk':'16bc0c98a9fc8-0be68b564974c3-37647e05-1fa400-16bc0c98a9fc8',
    #    '_hc.v':'78a71f2d-b242-c86d-97d1-01527c97daa0.1562307562',
    #    's_ViewType':'10',
    #    'aburl':'1',
    #    'cy':'2',
    #    'cye':'beijing',
    #    '_lxsdk_s':'16c6091a4d2-413-184-8b9%7C%7C8'
    #}
    cookies = {
        '_lxsdk_cuid':'16c6ee15815c8-0cdd3e898fd4cc-37647e05-fa000-16c6ee15815c8',
        '_lxsdk':'16c6ee15815c8-0cdd3e898fd4cc-37647e05-fa000-16c6ee15815c8',
        '_hc.v':'92a6974b-4405-d0a2-cc8f-45006650c8ba.1565228358',
        's_ViewType':'10',
        'aburl':'1',
        'cy':'2',
        'cye':'beijing',
        '_lxsdk_s':'16c6ee15819-bde-1d3-d0%7C%7C68'
    }

    print('当前请求的URL:%s'%url)
    print('当前使用的Method:%s'%method)
    print(params)
    print('当前使用的User-Agent:%s'%ua)

    for j in range(5):
        try:
            proxies = get_proxies()
            print('\t第%d次尝试请求, 使用的Proxy:%s'%(j, proxies['http']))
            if method == 'GET':
                result = requests.get(url, headers=headers, proxies=proxies, timeout=5, params=params, cookies=cookies)
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
        else:
            print('\t返回结果:%s\n' %result.text)

        break

    return result


#shopId = 98274270,
#shopId = 113511472,
#shopId = 98286173,
shopId = 121237887
cityId = 2
params = {
    "shopId":shopId,
    "cityId":cityId,
    "mainCategoryId":132,
    #"_token":"eJxVjltvgkAQhf/LvHYDs7sIK4kPxrZWUzQiorXhAS9FQrmUJcVL+t87RvvQZJIz8805yblAPdqByxHR4gy+9zW4wA00bGDQaPp07I4QitvCQWSw/cdkVxDb1OEjuO9cKGRSyuhKfAI3ohAjdlsdR0VMWDRXz4gscGiayjXNtm2NXRoXVVokxrbMTX0oK7OrhLK5I6kKUCIPKEGa3TW+a/N3e9SdvDpNCtr242Mw15b++vA9HYTzE0rv/DKZvj59Ts4nNRj4STy0s3D9MFv1x/nyOXtbrstNfszK/mqxmA5nvR78/ALTpE9/",
    #"uuid":"78a71f2d-b242-c86d-97d1-01527c97daa0.1562307562",
    "_token":"eJxVj0tvgzAQhP/LXmuB1xjbIOVQpRVNVBKVINSHciCPAqIhBGjzqPrfuzTJoZKlnf08M7K/oRmtwEfOuUQGX+sGfECLWwoYdC3duMoVwkM0RhkGy3/Mk8pjsGiSO/DfUBjO0OXznkQEzsRwImeptZkzIen0nhFZIO+62rft/X5vrYq0qosqs5bbjd3m29pGdFxEqQW9BSiyifuIUYoaCBnlXoW8CETmcBJaa+ZoEkoI9pd3PckM9i1l30Izvczuuof0dXK2RVaRWo8P8ayV7e49Cts4mR25E54eJtPH+4/J6WiGwyhLA1UmrzdPz9m4CA67NMiLxSYqt7fp58t0kg0G8PMLb8hbbw==",
    "uuid":"92a6974b-4405-d0a2-cc8f-45006650c8ba.1565228358",
    "platform":1,
    "partner":150,
    "optimusCode":10,
    "originUrl":"http://www.dianping.com/shop/%d" %shopId,
}

url = "http://www.dianping.com/ajax/json/shopDynamic/reviewAndStar"
result = do_request(url, method='GET', params=params)

d_map = {
    '\ue32b':'0',
    '1':'1',
    '\uef77':'2',
    '\uf200':'3',
    '\uef11':'4',
    '\uefab':'5',
    '\ue887':'6',
    '\ue594':'7',
    '\uf537':'8',
    '\uecb6':'9',
}

def get_svg_int(html):
    int_arr = []
    html = html.replace('1<d', '<d class="num">1</d><d')
    html = html.replace('d>1<d', 'd><d class="num">1</d><d')
    html = html.replace('d>1', 'd><d class="num">1</d>')
    soup = BeautifulSoup(html, 'html.parser')
    d_html = soup.findAll('d')
    for i in range(len(d_html)):
        int_arr.append(d_map[d_html[i].get_text()])
    int_str = ''.join(int_arr)
    print('svg int:', int_str)

def get_svg_float(html):
    float_arr = []
    html = html.replace('.1', '.<d class="num">1</d>')
    html = html.replace('1.', '<d class="num">1</d>.')
    soup = BeautifulSoup(html, 'html.parser')
    d_html = soup.findAll('d')
    for i in range(len(d_html)):
        float_arr.append(d_map[d_html[i].get_text()])
    float_str = '.'.join(float_arr)
    print('svg float:', float_str)

get_svg_int(json.loads(result.text)['avgPrice'])
get_svg_int(json.loads(result.text)['defaultReviewCount'])
get_svg_float(json.loads(result.text)['shopRefinedScoreValueList'][0])
get_svg_float(json.loads(result.text)['shopRefinedScoreValueList'][1])
get_svg_float(json.loads(result.text)['shopRefinedScoreValueList'][2])



avg_price_arr = []
review_count_arr = []
flavor_score_arr = []
surrounding_score_arr = []
service_score_arr = []


avg_price_html = json.loads(result.text)['avgPrice']
avg_price_html = avg_price_html.replace('1<d', '<d class="num">1</d><d')
avg_price_html = avg_price_html.replace('d>1<d', 'd><d class="num">1</d><d')
avg_price_html = avg_price_html.replace('d>1', 'd><d class="num">1</d>')
soup = BeautifulSoup(avg_price_html, 'html.parser')
d_html = soup.findAll('d')
for i in range(len(d_html)):
    avg_price_arr.append(d_map[d_html[i].get_text()])
avg_price = ''.join(avg_price_arr)
print('avg price:', avg_price)

review_count_html = json.loads(result.text)['defaultReviewCount']
review_count_html = review_count_html.replace('1<d', '<d class="num">1</d><d')
review_count_html = review_count_html.replace('d>1<d', 'd><d class="num">1</d><d')
review_count_html = review_count_html.replace('d>1', 'd><d class="num">1</d>')
soup = BeautifulSoup(review_count_html, 'html.parser')
d_html = soup.findAll('d')
for i in range(len(d_html)):
    review_count_arr.append(d_map[d_html[i].get_text()])
review_count = ''.join(review_count_arr)
print('review count:', review_count)

flavor_score_html = json.loads(result.text)['shopRefinedScoreValueList'][0]
flavor_score_html = flavor_score_html.replace('.1', '.<d class="num">1</d>')
flavor_score_html = flavor_score_html.replace('1.', '<d class="num">1</d>.')
soup = BeautifulSoup(flavor_score_html, 'html.parser')
d_html = soup.findAll('d')
for i in range(len(d_html)):
    flavor_score_arr.append(d_map[d_html[i].get_text()])
flavor_score = '.'.join(flavor_score_arr)
print('flavor score:', flavor_score)

surrounding_score_html = json.loads(result.text)['shopRefinedScoreValueList'][1]
surrounding_score_html = surrounding_score_html.replace('.1', '.<d class="num">1</d>')
surrounding_score_html = surrounding_score_html.replace('1.', '<d class="num">1</d>.')
soup = BeautifulSoup(surrounding_score_html, 'html.parser')
d_html = soup.findAll('d')
for i in range(len(d_html)):
    surrounding_score_arr.append(d_map[d_html[i].get_text()])
surrounding_score = '.'.join(surrounding_score_arr)
print('surrounding score:', surrounding_score)

service_score_html = json.loads(result.text)['shopRefinedScoreValueList'][2]
service_score_html = service_score_html.replace('.1', '.<d class="num">1</d>')
service_score_html = service_score_html.replace('1.', '<d class="num">1</d>.')
soup = BeautifulSoup(service_score_html, 'html.parser')
d_html = soup.findAll('d')
for i in range(len(d_html)):
    service_score_arr.append(d_map[d_html[i].get_text()])
service_score = '.'.join(service_score_arr)
print('service score:', service_score)
