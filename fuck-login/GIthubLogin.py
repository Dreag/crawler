# -*- coding: utf-8 -*
import requests
from lxml import html

LOGIN_URL = "https://github.com/login"
SESSION_URL = "https://github.com/session"

s = requests.session()
r = s.get(LOGIN_URL)

tree = html.fromstring(r.text)
el = tree.xpath('//input[@name="authenticity_token"]')[0]

authenticity_token = el.attrib['value']

data = {
    'commit': 'Sign in',
    'utf8':'√',
    'authenticity_token': authenticity_token,
    'login': 'yang_g1@126.com',
    'password': 'gy.970802..'
}

r = s.post(SESSION_URL, data=data)

print(r)

tree = html.fromstring(r.text)
el = tree.xpath('//ul[@class="mini-repo-list js-repo-list"]')[0]
el.xpath('//li[contains(@class, "public")]')
print (el.xpath('//span[@class="repo"]')[0].text)

#print tree.xpath('//ul[@class="mini-repo-list js-repo-list"]//li[contains(@class, "public")]//\span[@class="repo"]')[0].text
