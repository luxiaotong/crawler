import execjs
import demjson
import pandas as pd

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
            data_one = [k1, p, k2, c, k3, d]
            dist_arr.append(data_one)

label = ['pcode', 'p', 'ccode', 'c', 'dcode', 'd']
df = pd.DataFrame(dist_arr, columns=label)
df.to_csv('dist.csv')
print('Done!')
