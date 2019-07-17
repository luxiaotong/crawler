import requests
import pandas as pd
from bs4 import BeautifulSoup


# 获取全部省份
result = requests.get('http://www.luyuan.cn/index.php/service.html')
service_html = result.text
soup = BeautifulSoup(service_html, 'html.parser')
sel_region_html = soup.find(id="sel_region").findAll('option')
province_code_arr = []
province_raws = []
for i in range(1, len(sel_region_html)):
    province_name = sel_region_html[i].string
    province_code = sel_region_html[i]['value']
    province_code_arr.append(province_code)

    province_one = [
        province_code,
        province_name,
    ]
    province_raws.append(province_one)

province_df = pd.DataFrame(province_raws, columns=['province code', 'province name'])
province_df.to_csv('lvyuan_province.csv')
print(province_df)

# 遍历省份-获取每个省份的全部城市ID
city_code_arr = []
city_raws = []
for i in range(len(province_code_arr)):
    province_code = province_code_arr[i]
    result = requests.get('http://www.luyuan.cn/index.php/mapdealer/change_resion/%s'%province_code)
    region_html = result.text
    soup = BeautifulSoup(region_html, 'html.parser')
    option_html = soup.findAll('option')
    for i in range(len(option_html)):
        city_name = option_html[i].string
        city_code = option_html[i]['value']
        city_code_arr.append(city_code)

        city_one = [
            province_code,
            city_code,
            city_name,
        ]
        city_raws.append(city_one)

city_df = pd.DataFrame(city_raws, columns=['province code', 'city code', 'city name'])
city_df.to_csv('lvyuan_city.csv')
print(city_df)

# 遍历城市-获取每个城市ID对应的门店
data_raws = []
#city_code_arr = [110100]
for i in range(len(city_code_arr)):
    city_code = city_code_arr[i]
    result = requests.get('http://www.luyuan.cn/index.php/mapdealer/jxs_resion/%s/0'%city_code)
    jxs_html = result.text
    soup = BeautifulSoup(jxs_html, 'html.parser')
    li_html = soup.findAll('li')
    for i in range(len(li_html)-1):
        data_one = [
            city_code,
            li_html[i]['data-title'],
            li_html[i]['data-address'],
            li_html[i]['data-telphone'],
            li_html[i]['data-jin'],
            li_html[i]['data-wei'],
        ]
        data_raws.append(data_one)
label = ['cityid', 'title', 'address', 'mobile', 'longitude', 'latitude']
store_df = pd.DataFrame(data_raws, columns=label)
store_df.to_csv('lvyuan.csv')
print(store_df)
