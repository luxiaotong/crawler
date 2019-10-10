import pandas as pd
import mysql.connector as sql

org_db = sql.connect(host='127.0.0.1', database='crawler', user='root')
org_cursor = org_db.cursor(dictionary=True)

org_a_df = pd.read_csv('org_a.csv')
org_a_arr = org_a_df.values.tolist()
print(org_a_arr)
sql = "INSERT INTO science_net_org (name, city, dept, level) VALUES (%s, %s, %s, 'A')"
org_cursor.executemany(sql, org_a_arr)

org_b_df = pd.read_csv('org_b.csv')
org_b_arr = org_b_df.values.tolist()
print(org_b_arr)
sql = "INSERT INTO science_net_org (name, city, dept, level) VALUES (%s, %s, %s, 'B')"
org_cursor.executemany(sql, org_b_arr)

org_c_df = pd.read_csv('org_c.csv')
org_c_arr = org_c_df.values.tolist()
print(org_c_arr)
sql = "INSERT INTO science_net_org (name, city, dept, level) VALUES (%s, %s, %s, 'C')"
org_cursor.executemany(sql, org_c_arr)

org_db.commit()
