# -*- coding: utf-8 -*
import requests
#from lxml import html
from bs4 import BeautifulSoup

LOGIN_URL = "https://www.zhihu.com"
SESSION_URL = "https://www.zhihu.com/login/"

headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}
s = requests.session()
r = s.get(LOGIN_URL,headers = headers)

# tree = html.fromstring(r.text)
demo = r.text
soup = BeautifulSoup(demo,"html.parser")

xsrf = soup.find(attrs={"name":"_xsrf"}).get("value")
# el = tree.xpath('//input[@name="_xsrf"]')

# xsrf = el.attrib['value']

data = {
        'phone_num': "15237107089",
        'password': "gy.970802..zh",
        '_xsrf': xsrf,
        "captcha_type": "cn",
        'remember_me': 'true'
}

r = s.post(SESSION_URL, data=data)
print(r)