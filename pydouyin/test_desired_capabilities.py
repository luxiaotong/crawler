from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import json
import time
from browsermobproxy import Server
from urllib.parse import urlparse


share_id = "83834087816"
share_url = "https://www.iesdouyin.com/share/user/"+share_id


# Chrome
caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}
chrome_options = Options()
chrome_options.set_headless(headless=True)
douyin_driver = webdriver.Chrome(options=chrome_options, desired_capabilities=caps)


douyin_driver.get(share_url)


def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']
    print(response)
    return response


browser_log = douyin_driver.get_log('performance') 
events = [process_browser_log_entry(entry) for entry in browser_log]


douyin_driver.quit()
