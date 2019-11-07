from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from utils import have_a_rest
import random
import json

server = Server("./browsermob-proxy-2.1.4/bin/browsermob-proxy", {'port': 9999})
server.start()
proxy = server.create_proxy()
url = urlparse(proxy.proxy).path

chrome_options = Options()
chrome_options.set_headless(headless=True)
chrome_options.add_argument("--proxy-server={0}".format(url))
douyin_driver = webdriver.Chrome(options=chrome_options)


short_url = 'http://v.douyin.com/H3nPbo/'
douyin_driver.get(short_url)

have_a_rest(random.randrange(3, 5, 1))
soup = BeautifulSoup(douyin_driver.page_source, 'html.parser')
user_id = soup.find('span', class_='focus-btn')['data-id']
print(user_id)


proxy.new_har("load_post_page", options={'captureHeaders': True, 'captureContent':True})

post_tab = douyin_driver.find_element_by_css_selector("div.user-tab.tab.get-list")
#post_tab = douyin_driver.find_element_by_class_name('user-tab')
#ActionChains(douyin_driver).click(post_tab).perform()
douyin_driver.execute_script('arguments[0].click();', post_tab)
have_a_rest(random.randrange(3, 5, 1))

# Process Response Content
har_return = json.loads(json.dumps(proxy.har, ensure_ascii=False))
entries = har_return['log']['entries']
for i in range(len(entries)):
    if '/web/api/v2/aweme/post/' in entries[i]['request']['url']:
        print(entries[i]['request']['url'])
        result = json.loads(entries[i]['response']['content']['text'])

print(result)


have_a_rest(random.randrange(10, 20, 1))
server.stop()
douyin_driver.quit()
