import requests
import json
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

dist_df = pd.read_csv('dist.csv')
pcode_arr = np.array(dist_df.drop_duplicates(['pcode'])['pcode'])

data_rows = []
for i in range(len(pcode_arr)):
    post_data = {
        'province_id': pcode_arr[i],
        'pageindex': 0,
        'latitude': 39.911013,
        'longitude': 116.413554,
    }

    while True:
        post_data['pageindex'] += 1
        result = requests.post('http://wx.supersoco.com/index.php?c=MapCtrl&m=getsupplierlist_page', data=post_data)
    
        list_result = json.loads(result.text)
    
        for i in range(len(list_result['result'])):
            data_one = [
                list_result['result'][i]['id'],
                list_result['result'][i]['title'],
                list_result['result'][i]['address'],
                list_result['result'][i]['lbs_type'],
                list_result['result'][i]['longitude'],
                list_result['result'][i]['latitude'],
                list_result['result'][i]['province_id'],
                list_result['result'][i]['province'],
                list_result['result'][i]['city_id'],
                list_result['result'][i]['city'],
                list_result['result'][i]['county_id'],
                list_result['result'][i]['county'],
                list_result['result'][i]['contact_manager'],
                list_result['result'][i]['tel'],
                list_result['result'][i]['bus_hour_start'],
                list_result['result'][i]['bus_hour_end'],
                list_result['result'][i]['updatetime'],
            ]
            data_rows.append(data_one)
            print(data_one)
    
        if len(list_result['result']) < 10: break


label = [
        'id', 'title', 'address', 'lbs_type', 'longitude', 'latitude',
        'province_id', 'province', 'city_id', 'city',
        'county_id', 'county', 'contact_manager', 'tel',
        'bus_hour_start', 'bus_hour_end', 'updatetime',
        ]
store_df = pd.DataFrame(data_rows, columns=label)
store_df.to_csv('soco.csv')
print('Done!')
