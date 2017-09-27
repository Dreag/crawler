# author:gaoyang
# time:2017.9.21

import requests
import json
from bs4 import BeautifulSoup


def get_pagenum(citylist, headers):
    pages = {}
    url = "http://piao.qunar.com/ticket/list.htm?from=mpshouye_theme&keyword=必游景点&region={}&page=1"
    for city in citylist:
        r = requests.get(url.format(city), headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        html = r.text
        soup = BeautifulSoup(html, "html.parser")
        sight_acount = soup.find("div", {"id": "pager-container"}).get("data-total-count")
        pages[city] = int(int(sight_acount) / 15) + 1
    return pages


def download(url, citylist, pagenum, headers):
    index = []
    # 遍历整个列表里的城市
    for city in citylist:
        # 遍历每个城市热门景点
        print(pagenum[city]+1)
        for i in range(pagenum[city] + 1)[1:]:
            r = requests.get(url.format(city, i), headers=headers)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            html = r.text
            soup = BeautifulSoup(html, "html.parser")
            get_link(soup)
    return index


def get_link(soup):
    indexlist = {}
    result_list = soup.find("div", {"class": "result_list"})
    sight_item_about = result_list.find_all("div", {"class": "sight_item_about"})
    sight_item_pop = result_list.find_all("div", {"class": "sight_item_pop"})

    for l, p in zip(sight_item_about, sight_item_pop):
        information = []
        title = l.find("a").get('title')
        try:
            level = l.find("span", {"class": "level"}).string
        except:
            level = "非A级景区"

        href = "piao.qunar.com" + l.find("a").get('href')
        # href：景点详情页的信息，level：景点的评级,title:景点名称，intro：景点的简介
        intro = l.find("div", {"class": "intro color999"}).get("title")
        try:
            sales = p.find("span", {"class": "hot_num"}).string
        except:
            sales = "0"
        information.append(href)
        information.append(level)
        information.append(intro)
        information.append(sales)
        indexlist[title] = information
    index.append(indexlist)


cities = ["北京", "上海", "成都", "三亚", "广州", "重庆", "深圳", "西安", "杭州", "厦门", "武汉", "大连", "苏州", "青岛", "天津", "南京", "香港", "桂林",
          "郑州", "昆明"]

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87'}

url = "http://piao.qunar.com/ticket/list.htm?from=mpshouye_theme&keyword=必游景点&region={}&page={}"

index = []
pagenum = get_pagenum(cities, headers)
informations = download(url, cities, pagenum, headers)
print(informations)

with open("sight_link.json", "r+", encoding="utf-8") as f:
    f.write(json.dumps(index))
