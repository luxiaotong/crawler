import requests
import json
import pandas as pd

key = ''
keywords = '爱玛电动车'
result = requests.get('https://restapi.amap.com/v3/place/text?key=%s&keywords=%s'%(key, keywords))
result = json.loads(result.text)
city_list = result['suggestion']['cities']
data_rows = []
for i in range(len(city_list)):
    adcode = city_list[i]['adcode']
    page = 0
    while True:
        page += 1
        result = requests.get('https://restapi.amap.com/v3/place/text?key=%s&keywords=%s&city=%s&page=%s&citylimit=true'%(key, keywords, adcode, page))
        result = json.loads(result.text)
        poi_list = result['pois']

        for i in range(len(poi_list)):
            data_one = [
                poi_list[i]['id'],
                poi_list[i]['name'],
                poi_list[i]['address'],
                poi_list[i]['location'],
                poi_list[i]['pname'],
                poi_list[i]['cityname'],
                poi_list[i]['adname'],
                poi_list[i]['tel'],
                poi_list[i]['type'],
                poi_list[i]['typecode'],
            ]
            data_rows.append(data_one)
            print(data_one)

        if len(poi_list) < 20: break


label = [ 'id', 'name', 'address', 'location', 'pname', 'cityname', 'adname', 'tel', 'type', 'typecode', ]
store_df = pd.DataFrame(data_rows, columns=label)
store_df.to_csv('aima.csv')
print('Done!')
