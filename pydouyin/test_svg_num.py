import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time
import pandas as pd

num_map = {
    #0
    ' \ue603 ':'0',
    ' \ue60d ':'0',
    ' \ue616 ':'0',
    #1
    ' \ue602 ':'1',
    ' \ue60e ':'1',
    ' \ue618 ':'1',
    #2
    ' \ue605 ':'2',
    ' \ue610 ':'2',
    ' \ue617 ':'2',
    #3
    ' \ue604 ':'3',
    ' \ue611 ':'3',
    ' \ue61a ':'3',
    #4
    ' \ue606 ':'4',
    ' \ue60c ':'4',
    ' \ue619 ':'4',
    #5
    ' \ue607 ':'5',
    ' \ue60f ':'5',
    ' \ue61b ':'5',
    #6
    ' \ue608 ':'6',
    ' \ue612 ':'6',
    ' \ue61f ':'6',
    #7
    ' \ue60a ':'7',
    ' \ue613 ':'7',
    ' \ue61c ':'7',
    #8
    ' \ue60b ':'8',
    ' \ue614 ':'8',
    ' \ue61d ':'8',
    #9
    ' \ue609 ':'9',
    ' \ue615 ':'9',
    ' \ue61e ':'9',
}

def get_post_num(post_num_html):
    post_num_arr = []
    for i in range(len(post_num_html.contents)):
        post_num_content = post_num_html.contents[i]
        if post_num_content == ' ': continue
        if post_num_content != '.' and post_num_content != 'w ':
            post_num_arr.append(num_map[post_num_content.get_text()])
        else:
            post_num_arr.append(post_num_content)
    return ''.join(post_num_arr)

def get_like_num(like_num_html):
    like_num_arr = []
    for i in range(len(like_num_html.contents)):
        like_num_content = like_num_html.contents[i]
        if like_num_content == ' ': continue
        if like_num_content != '.' and like_num_content != 'w ':
            like_num_arr.append(num_map[like_num_content.get_text()])
        else:
            like_num_arr.append(like_num_content)
    return ''.join(like_num_arr)

def get_focus_num(focus_num_html):
    focus_num_arr = []
    for i in range(len(focus_num_html.contents)):
        focus_num_content = focus_num_html.contents[i]
        if focus_num_content == ' ': continue
        if focus_num_content != '.' and focus_num_content != 'w ':
            focus_num_arr.append(num_map[focus_num_content.get_text()])
        else:
            focus_num_arr.append(focus_num_content)
    return ''.join(focus_num_arr)

def get_follow_num(follow_num_html):
    follow_num_arr = []
    for i in range(len(follow_num_html.contents)):
        follow_num_content = follow_num_html.contents[i]
        if follow_num_content == ' ': continue
        if follow_num_content != '.' and follow_num_content != 'w ':
            follow_num_arr.append(num_map[follow_num_content.get_text()])
        else:
            follow_num_arr.append(follow_num_content)
    return ''.join(follow_num_arr)

def get_digg_num(digg_num_html):
    digg_num_arr = []
    for i in range(len(digg_num_html.contents)):
        digg_num_content = digg_num_html.contents[i]
        if digg_num_content == ' ': continue
        if digg_num_content != '.' and digg_num_content != 'w ':
            digg_num_arr.append(num_map[digg_num_content.get_text()])
        else:
            digg_num_arr.append(digg_num_content)
    return ''.join(digg_num_arr)


#分享ID
share_id = "83834087816" #6722315998835330318
#share_id = "68544493839" #6720499432518929672
#share_id = "94417447197" #6722733418410560772
share_url = "https://www.iesdouyin.com/share/user/"+share_id
header = {
    "User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"
}
response = requests.get(url=share_url,headers=header)
aweme_post_html = response.text

soup = BeautifulSoup(aweme_post_html, 'html.parser')
post_num_html = soup.find('div', class_='user-tab').find('span')
like_num_html = soup.find('div', class_='like-tab').find('span')
focus_num_html = soup.find('span', class_='focus').find('span')
follow_num_html = soup.find('span', class_='follower').find('span')
digg_num_html = soup.find('span', class_='liked-num').find('span')


post_num = get_post_num(post_num_html)
print('作品:', post_num)
like_num = get_like_num(like_num_html)
print('喜欢:', like_num)
focus_num = get_focus_num(focus_num_html)
print('关注:', focus_num)
follow_num = get_follow_num(follow_num_html)
print('粉丝:', follow_num)
digg_num = get_digg_num(digg_num_html)
print('获赞:', digg_num)
