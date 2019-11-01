from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import json
import time
from urllib.parse import urlparse
import random

from dy_parse import DYParse
from utils import have_a_rest

class DYCrawler:

    def __init__(self):
        # Browsermob Proxy
        self.server = Server("./browsermob-proxy-2.1.4/bin/browsermob-proxy", {'port': 9999})
        self.server.start()
        self.proxy = self.server.create_proxy()
        url = urlparse(self.proxy.proxy).path

        # Selenium Chrome
        chrome_options = Options()
        chrome_options.set_headless(headless=True)
        #mobile_emulation = { "deviceName": "Nexus 5" }
        #chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        chrome_options.add_argument("--proxy-server={0}".format(url))
        self.douyin_driver = webdriver.Chrome(options=chrome_options)

        self.parse = DYParse()

    def __del__(self):
        # Quit
        self.server.stop()
        self.douyin_driver.quit()

    def run(self, model):
        share_url = "https://www.iesdouyin.com/share/user/" + model.user_id
        page_num = 1

        # Load First Page
        self.proxy.new_har("load_first_page", options={'captureHeaders': True, 'captureContent':True})
        self.douyin_driver.get(share_url)
        print("...........Ready to Load Page ", page_num)

        # Process User Data
        user_data = self.parse.process_user_data(self.douyin_driver.page_source)
        model.add_user_statistics(user_data)

        # Process Response Content & Load More
        while True:
            # Take a break
            have_a_rest(random.randrange(3, 5, 1))
        
            # Process Response Content
            har_return = json.loads(json.dumps(self.proxy.har, ensure_ascii=False))
            entries = har_return['log']['entries']
            for i in range(len(entries)):
                if '/web/api/v2/aweme/post/' in entries[i]['request']['url']:
                    print(entries[i]['request']['url'])
                    result = json.loads(entries[i]['response']['content']['text'])
        
            if len(result['aweme_list']) == 0:
                break
            # Process Post Data
            model.add_post(result['aweme_list'])
            model.add_post_statistics(result['aweme_list'])
        
            # Whether to Load Next Page
            #print(result['aweme_list'][-1]['aweme_id'])
            #print(result['has_more'])
            if result['aweme_list'][-1]['aweme_id'] < model.min_aweme_id:
                break
            if result['has_more'] == False:
                break
        
            # Load Next Page
            have_a_rest(random.randrange(5, 10, 1))
            self.proxy.new_har("load_next_page", options={'captureHeaders': True, 'captureContent':True})
            print("...........Ready to Load Page ", page_num)
            # 拖动到可见的元素去
            pageload_element = self.douyin_driver.find_element_by_id("pagelet-loading")
            self.douyin_driver.execute_script("arguments[0].scrollIntoView();", pageload_element)
            print("...........Scrolled")
            page_num += 1

    # 获取话题中的aweme_id
    def run_topic(self, model):
        topic_url = "https://www.iesdouyin.com/share/challenge/1644976955930631/?u_code=153ih74hk&utm_campaign=client_share&app=aweme&utm_medium=ios&tt_from=copy&utm_source=copy"
        page_num = 1

        # Load First Page
        #self.proxy.new_har("load_first_page", options={'captureHeaders': True, 'captureContent':True})
        self.douyin_driver.get(topic_url)
        print("...........Ready to Load Page ", page_num)

        # Process Topic Post
        have_a_rest(20)
        #topic_post = self.parse.process_topic_post(self.douyin_driver.page_source)
        #model.add_topic_post(topic_post)
        #print(topic_post)
        self.douyin_driver.save_screenshot("./topic1.png")#图片是为了比较变化



        pageload_element = self.douyin_driver.find_element_by_id("pagelet-loading")
        self.douyin_driver.execute_script("arguments[0].scrollIntoView();", pageload_element)
        print("*"*10, "Scrolled", "*"*10)
        print("*"*10, "Loading", "*"*10)

        have_a_rest(200)
        #print("PageSource:")
        #print(self.douyin_driver.page_source)
        self.douyin_driver.save_screenshot("./topic2.png")#图片是为了比较变化

        page_num += 1
