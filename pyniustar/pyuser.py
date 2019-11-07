import pandas as pd
from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from utils import have_a_rest
import random
import json
from niustar_model import NiuStarModel

model = NiuStarModel()

# Load User
#user_df = pd.read_excel('./niustar_user_20191101.xlsx')
#user_df = pd.read_excel('./niustar_user_20191104.xlsx')
user_df = pd.read_excel('./niustar_user_20191105.xlsx')


server = Server("./browsermob-proxy-2.1.4/bin/browsermob-proxy", {'port': 9999})
server.start()
proxy = server.create_proxy()
url = urlparse(proxy.proxy).path

chrome_options = Options()
chrome_options.set_headless(headless=True)
chrome_options.add_argument("--proxy-server={0}".format(url))
douyin_driver = webdriver.Chrome(options=chrome_options)

for index, row in user_df.iterrows():

    short_url = row[2].strip()
    douyin_driver.get(short_url)

    # Process Response Content
    have_a_rest(random.randrange(3, 5, 1))
    soup = BeautifulSoup(douyin_driver.page_source, 'html.parser')

    music_active = soup.find('div', class_='music-tab tab active get-list')
    if music_active:
        proxy.new_har("load_post_page", options={'captureHeaders': True, 'captureContent':True})
        post_tab = douyin_driver.find_element_by_css_selector("div.user-tab.tab.get-list")
        douyin_driver.execute_script('arguments[0].click();', post_tab)
        have_a_rest(random.randrange(3, 5, 1))

        # Process Response Content
        har_return = json.loads(json.dumps(proxy.har, ensure_ascii=False))
        entries = har_return['log']['entries']
        for i in range(len(entries)):
            if '/web/api/v2/aweme/post/' in entries[i]['request']['url']:
                print(entries[i]['request']['url'])
                result = json.loads(entries[i]['response']['content']['text'])
        if len(result['aweme_list']) > 0:
            min_aweme_id = result['aweme_list'][0]['aweme_id']
        else:
            min_aweme_id = 0
    else:
        aweme_list = soup.findAll('li', class_='item goWork')
        if len(aweme_list) > 0:
            min_aweme_id = aweme_list[0]['data-id']
        else:
            min_aweme_id = 0

    user = {
        "user_id"       : soup.find('span', class_='focus-btn')['data-id'],
        "username"      : soup.find('p', class_='nickname').text.encode('utf-8'),
        "min_aweme_id"  : min_aweme_id,
        "avatar_url"    : soup.find('img', class_='avatar')['src'],
        "short_url"     : short_url,
        'gid'           : row[0],
        'douyin_account': row[1],
        'wechat_account': row[4],
        'realname'      : row[3],
    }

    model.add_user(user)
    print(user)
    have_a_rest(random.randrange(5, 10, 1))

douyin_driver.quit()
print("Crawler End to Run!")
