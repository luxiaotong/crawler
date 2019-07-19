import requests
import execjs
import json
import demjson

result = requests.get('https://www.yadea.com.cn/scripts/storeData.js')
js_obj = result.text.split("window._")[1][:-15]
print(js_obj[:100], js_obj[-100:])

f = open("data.js", "w")
f.write(js_obj)
f.close()


#js_obj = '{110000:{110100:{110101:[{code:"A0010015F43",name:"天坛东门雅迪",address:"东城体育馆路",tel:"13811011982",gps:"116.428847,39.89034",level:"二网",openTime:"8：00-19：00",isClose:"1"}]}}}'


# to
#py_obj = demjson.decode(js_obj)
#print(py_obj[110000][110100][110101][0])
