import execjs
import demjson
import requests
from urllib.parse import unquote
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en,zh;q=0.9",
    "Connection": "keep-alive",
    "Cookie": "UM_distinctid=16bfe8909f9a4b-0afcf6b805bab6-37647e05-1fa400-16bfe8909fa4ab; Hm_lvt_bab9524cb72f32892de60fd48af5f4aa=1563343522; CNZZDATA1271242693=749532626-1563338602-https%253A%252F%252Fwww.google.com%252F%7C1563591102; ASP.NET_SessionId=g1nzaaabsbnmk3bkomkmclbq; Hm_lpvt_bab9524cb72f32892de60fd48af5f4aa=1563591954"
}

f = open("TDES.js",'r',encoding = 'utf-8')
js = f.read()
f.close()
ctx = execjs.compile(js)

def encrpyt_data(p, c, d):
    p = ctx.call("TDES.encrypt", p)
    c = ctx.call("TDES.encrypt", c)
    d = ctx.call("TDES.encrypt", d)
    return p, c, d

def name_decode(s):
    return s.replace('%', '\\') \
            .encode('utf-8') \
            .decode('unicode_escape')

def get_data(p_name, c_name, d_name):
    p, c, d = encrpyt_data(p_name, c_name, d_name)
    data = {'cmd':'getDotList', 'p':p, 'c':c, 'd':d}
    result = requests.post('http://www.xinri.com/Ajax/AjaxHandler_XRDDC.ashx', data = data, headers=headers)
    info = unquote(demjson.decode(result.text)['info'], encoding='utf-8')
    soup = BeautifulSoup(info, 'html.parser')
    dl_arr = soup.findAll('dl')
    data_rows = []
    for i in range(len(dl_arr)):
        if dl_arr[i]['data-title'] == '': continue
        data_one = [
            name_decode(dl_arr[i]['data-title']),
            name_decode(dl_arr[i]['data-address']),
            dl_arr[i]['data-point'],
            dl_arr[i]['data-tel'],
            p_name,
            c_name,
            d_name,
        ]
        data_rows.append(data_one)
        print(data_one)
    return data_rows

f = open("data.js",'r',encoding = 'utf-8')
dist_js = f.read()
dist = demjson.decode(dist_js)
dist_arr = []

for k1 in dist[86]:
    if k1 not in dist: continue
    p = dist[86][k1]
    for k2 in dist[k1]:
        if k2 not in dist: continue
        c = dist[k1][k2]
        for k3 in dist[k2]:
            d = dist[k2][k3]
            dist_arr.extend(get_data(p, c, d))

df = pd.DataFrame.from_dict(dist_arr)
df.to_csv('xinri.csv')
print('Done!')
