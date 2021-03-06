from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import json
import time
from urllib.parse import urlparse
import random

from niustar_parse import NiuStarParse
from utils import have_a_rest

class NiuStarCrawler:

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

        self.parse = NiuStarParse()

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

        # Swtich to post tab
        music_active = self.parse.get_music_tab(self.douyin_driver.page_source)
        if music_active:
            self.proxy.new_har("load_first_page", options={'captureHeaders': True, 'captureContent':True})
            post_tab = self.douyin_driver.find_element_by_css_selector("div.user-tab.tab.get-list")
            self.douyin_driver.execute_script('arguments[0].click();', post_tab)

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
                model.check_post()
                break

            # Process Post Data
            model.add_post(result['aweme_list'])
            model.add_post_statistics(result['aweme_list'])

            # Whether to Load Next Page
            if result['aweme_list'][-1]['aweme_id'] < model.min_aweme_id:
                break
            if result['has_more'] == False:
                break

            # Load Next Page
            page_num += 1
            have_a_rest(random.randrange(5, 10, 1))
            self.proxy.new_har("load_next_page", options={'captureHeaders': True, 'captureContent':True})
            print("...........Ready to Load Page ", page_num)
            # 拖动到可见的元素去
            pageload_element = self.douyin_driver.find_element_by_id("pagelet-loading")
            self.douyin_driver.execute_script("arguments[0].scrollIntoView();", pageload_element)
            print("...........Scrolled")
