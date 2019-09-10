from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import json
import time
from browsermobproxy import Server
from urllib.parse import urlparse

share_id = "83834087816"
share_url = "https://www.iesdouyin.com/share/user/"+share_id

# Browsermob Proxy
server = Server("./browsermob-proxy-2.1.4/bin/browsermob-proxy")
server.start()
proxy = server.create_proxy()
url = urlparse(proxy.proxy).path

# Selenium Chrome
chrome_options = Options()
chrome_options.set_headless(headless=True)
chrome_options.add_argument("--proxy-server={0}".format(url))
douyin_driver = webdriver.Chrome(options=chrome_options)
proxy.new_har("iesdouyin", options={'captureHeaders': True, 'captureContent':True})

# Get & Return
douyin_driver.get(share_url)
result = json.loads(json.dumps(proxy.har, ensure_ascii=False))
entries = result['log']['entries']
for i in range(len(entries)):
    if '/web/api/v2/aweme/post/' in entries[i]['request']['url']:
        aweme_list = json.loads(entries[i]['response']['content']['text'])['aweme_list']

# Process Data
data = []
for i in range(len(aweme_list)):
    one_row = {
        'id': aweme_list[i]['aweme_id'],
        'desc': aweme_list[i]['desc'],
        'comment': aweme_list[i]['statistics']['comment_count'],
        'digg_count': aweme_list[i]['statistics']['digg_count'],
        'play_count': aweme_list[i]['statistics']['play_count'],
        'share_count': aweme_list[i]['statistics']['share_count'],
    }
    print(one_row)
    data.append(one_row)


server.stop()
douyin_driver.quit()
