import requests
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time
import pandas as pd



#分享ID
share_id = "83834087816"
share_url = "https://www.iesdouyin.com/share/user/"+share_id
header = {
    "User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"
}
response = requests.get(url=share_url,headers=header)

#dytk 和tac的正则表达式
dytk_search = re.compile(r"dytk: '(.*?)'")
tac_search = re.compile(r"<script>tac=(.*?)</script>")

#处理获取dytk 和tac
dytk = re.search(dytk_search,response.text).group(1)
tac = re.search(tac_search,response.text).group(1)

#tac封装成为js的格式
tac = "var tac="+tac+";"


# html页面的编写合成 header + tac+ foot
with open("head.txt") as f1:
    f1_read = f1.read()

with open("foot.txt") as f2:
    f2_read = f2.read().replace("&&&&", share_id)

with open("sign.html","w") as f_w:
    f_w.write(f1_read+"\n"+tac+"\n"+f2_read)

chrome_options = Options()
chrome_options.set_headless(headless=True)
douyin_driver = webdriver.Chrome(options=chrome_options)
douyin_driver.get("file:///Users/shannon/code/crawler/pydouyin/sign.html")

signature = douyin_driver.title
douyin_driver.quit()

print(dytk)
print(tac)
print(signature)

#curl 'https://www.iesdouyin.com/web/api/v2/aweme/post/?user_id=83834087816&sec_uid=&count=21&max_cursor=0&aid=1128&_signature=QvkTehAfH423nmOdOxyvrUL5E2&dytk=2f1f312f7325deb8244f711b1e230ae4' -H 'pragma: no-cache' -H 'cookie: _ga=GA1.2.868563206.1567557111; _gid=GA1.2.1730599626.1567661031; tt_webid=6733126270223779336; _ba=BA0.2-20190905-5199e-HPRYAtdrbOOHFZzjKX61' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: en,zh;q=0.9' -H 'user-agent: Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1' -H 'sec-fetch-mode: cors' -H 'accept: application/json' -H 'cache-control: no-cache' -H 'authority: www.iesdouyin.com' -H 'x-requested-with: XMLHttpRequest' -H 'sec-fetch-site: same-origin' -H 'referer: https://www.iesdouyin.com/share/user/83834087816' --compressed

movie_url = "https://www.iesdouyin.com/web/api/v2/aweme/post/?user_id=" + share_id + "&sec_uid=&count=21&max_cursor=0&aid=1128&_signature=" + signature + "&dytk=" + dytk
print(movie_url)

header = {
    "User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1",
    "pragma": "no-cache",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "accept": "application/json",
    "cache-control": "no-cache",
    "authority": "www.iesdouyin.com",
    "referer": "https://www.iesdouyin.com/share/user/83834087816",
    "x-requested-with": "XMLHttpRequest"
}

retry_count = 0
while True:
    retry_count += 1
    print(retry_count)

    movie_reponse = requests.get(url=movie_url,headers=header)
    aweme_list = json.loads(movie_reponse.text)["aweme_list"]
    if aweme_list == []:
        time.sleep(1)
        continue
    else:
        print(aweme_list)
        break
        #for item in aweme_list:
        #    video_url = item["video"]["play_addr"]["url_list"][0]
        #    video_response = requests.get(url=video_url,headers=header)
        #    with open("douyin.mp4","wb") as v:
        #        #不能使用video_response.text，必须使用content才可以把内容写进去
        #        v.write(video_response.content)
        #        break





#f = open("third.js",'r',encoding = 'utf-8')
#js = f.read()
#f.close()
#
#driver=webdriver.Chrome()
#driver.execute_script(js)
#result1 = driver.execute_script("return _bytedAcrawler.sign(arguments[0])", "110677980134")
#result2 = driver.execute_script("return _bytedAcrawler.sign(110677980134)")
#driver.close()
#
#print(result1)
#print(result2)

