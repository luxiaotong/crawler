import json
import pandas as pd
import mysql.connector as sql

code_db = sql.connect(host='127.0.0.1', database='crawler', user='root')
code_cursor = code_db.cursor(dictionary=True)

f = open("applycode.json",'r',encoding = 'utf-8')
code_json = f.read()
code_dict = json.loads(code_json)
f.close()

data = []
for i in range(len(code_dict)):
    subject_a   = code_dict[i]['label']
    subject_a_k = code_dict[i]['key']
    for j in range(len(code_dict[i]['children'])):
        subject_b   = code_dict[i]['children'][j]['label']
        subject_b_k = code_dict[i]['children'][j]['key']
        if 'children' in code_dict[i]['children'][j]:
            for k in range(len(code_dict[i]['children'][j]['children'])):
                subject_c   = code_dict[i]['children'][j]['children'][k]['label']
                subject_c_k = code_dict[i]['children'][j]['children'][k]['key']
                data_one = [
                    subject_a, subject_b, subject_c,
                    subject_a_k, subject_b_k, subject_c_k,
                ]
                print(data_one)
                data.append(data_one)
        else:
            data_one = [subject_a, subject_b, '', subject_a_k, subject_b_k, '']
            print(data_one)
            data.append(data_one)

sql = "INSERT INTO science_net_code (subject_a, subject_b, subject_c, subject_a_k, subject_b_k, subject_c_k) VALUES (%s, %s, %s, %s, %s, %s)"
code_cursor.executemany(sql, data)
code_db.commit()
