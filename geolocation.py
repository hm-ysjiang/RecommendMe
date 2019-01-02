from bs4 import BeautifulSoup as Bs
import json
import kcparser
import re
import requests

key = kcparser.get_ipstack_api_key()


def get_ip():
    r = requests.get('https://api.myip.com/')
    soup = Bs(r.text, 'html.parser')
    m = re.search(r'^{"ip":"(\d+\.\d+\.\d+\.\d+)",.+$', soup.get_text())
    if m:
        return m.group(1)


def get_location(ip):
    m = re.search(r'^\d+\.\d+\.\d+\.\d+$', ip)
    assert m
    global key
    r = requests.get(f'http://api.ipstack.com/{ip}?access_key={key}')
    js = json.loads(r.text)
    return js['latitude'], js['longitude']
