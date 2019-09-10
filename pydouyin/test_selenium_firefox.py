from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import json
import time
from browsermobproxy import Server
from urllib.parse import urlparse


share_id = "83834087816"
share_url = "https://www.iesdouyin.com/share/user/"+share_id


# Firefox
options = webdriver.FirefoxOptions()
#options.add_argument('-headless')
douyin_driver = webdriver.Firefox(firefox_options=options)

douyin_driver.get(share_url)

#douyin_driver.quit()
