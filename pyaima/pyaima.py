import requests
import json
import pandas as pd


store_list = []
for i in range(2, 33):
    result = requests.get('https://www.aimatech.com/outlets/list?ccode=0&pcode=%s'%i)
    result_json = result.text.split("(", 1)[1].strip(")")
    store_list.extend(json.loads(result_json))

store_df = pd.DataFrame.from_dict(store_list)
store_df.to_csv('aimatech.csv')
print(store_df)
