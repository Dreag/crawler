# -*- coding: utf-8 -*-

'''
    _author_: Gao Yang
    _time_:2017.8.25
'''

import urllib.request
import csv
import json
import lxml.html
import lxml.cssselect
import time


def download(url, num_retries=2):
    headers = {"User-Agent": "wswp"}
    request = urllib.request.Request(url,headers=headers)
    try:
        # 将网页进行编码
        fixed_html = urllib.request.urlopen(request).read().decode()

    except urllib.request.URLError as e:
        print('Download error:',e.reason)
        fixed_html = None

        if num_retries > 0:
            if hasattr(e,'code') and 500 <=e.code < 600:
                # retry 5xx HTTP errors
                return download(url,num_retries-1)
    return fixed_html


def crawlercountry(url):
    FIELDS = ('area', 'population', 'iso', 'country', 'capital', 'continent', 'tld', 'currency_code', 'currency_name', 'phone','postal_code_format', 'postal_code_regex', 'languages', 'neighbours')
    country = {k:"" for k in FIELDS}
    html = download(url)
    tree = lxml.html.fromstring(html)
    for field in FIELDS:
        td = tree.cssselect('table > tr#places_'+field+'__row > td.w2p_fw')[0]
        field_text = td.text_content()
        country[field] = field_text
    return country


def get_counname(countries):
    # 通过网页逆向工程得到AJAX数据
    html = download('http://example.webscraping.com/places/ajax/search.json?&page=0&page_size=1000&search_term=.')
    ajax = json.loads(html)
    for record in ajax['records']:
        countries.add(record['country'])
    countries = sorted(countries)
    # 将得到的所以国家的名字存储到country.txt文件中
    with open('/home/cherry963/PycharmProjects/Python/crawler/all_country/country.txt','r+',encoding='utf-8') as f:
        f.write(str(sorted(countries)))


def get_couninfo(url):
    number = 1
    # 遍历集合countries中的国家information
    for country in countries:
        time.sleep(10)
        # 网站的网页格式为http://example.webscraping.com/places/default/view/country-x
        full_url = url + country + "-" + str(number)
        # 得到完整的站点域名后，通过lxml解析特定的标签，并将得到的字典添加到数组attr中
        attr.append(crawlercountry(full_url))
        # 在数组attr中遍历每一个国家的FIELD中的key，得到列表row
        row = [attr[number-1][field] for field in FIELDS]
        print(row)
        # 写入csv文件
        writer.writerow(row)
        number += 1

if __name__ == '__main__':
    countries = set()
    attr = []
    url = "http://example.webscraping.com/places/default/view/"
    FIELDS = ('country', 'area', 'population', 'iso', 'capital', 'continent', 'tld', 'currency_code', 'currency_name', 'phone', 'languages')
    writer = csv.writer(open('/home/cherry963/PycharmProjects/Python/crawler/all_country/country.csv', 'r+',encoding='utf-8'))
    writer.writerow(FIELDS)
    get_counname(countries)
    get_couninfo(url)