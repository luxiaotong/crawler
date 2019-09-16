import sys
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from dy_model import DYModel

short_url = sys.argv[1]

chrome_options = Options()
chrome_options.set_headless(headless=True)
douyin_driver = webdriver.Chrome(options=chrome_options)
douyin_driver.get(short_url)

soup = BeautifulSoup(douyin_driver.page_source, 'html.parser')
user = {
    "user_id": soup.find('span', class_='focus-btn')['data-id'],
    "username": soup.find('p', class_='nickname').text,
    "avatar_url": soup.find('img', class_='avatar')['src'],
    "short_url": short_url,
}

model = DYModel()
model.add_user(user)
print(user)

douyin_driver.quit()
