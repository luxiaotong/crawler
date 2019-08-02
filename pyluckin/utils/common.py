import random
import json
import requests

def random_ua():
    with open('./utils/fake_useragent_0.1.11.json', 'r') as f:
        fake_ua = json.load(f)
    
    browser = random.choice(list(fake_ua['randomize'].values()))
    ua = random.choice(fake_ua['browsers'][browser])

    return ua

def get_proxy():
    result = requests.get('http://127.0.0.1:5010/get')
    return result.text

def get_proxies():
    proxies = {
        "http": get_proxy(),
        "https": get_proxy()
    }
    return proxies
