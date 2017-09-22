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
    print(pages)
    return pages

def download(url,citylist, pagenum, headers):
    index = []
    for city in citylist:
        indexlist = {}
        for i in range(pagenum[city] + 1)[1:]:
            r = requests.get(url.format(city, i), headers=headers)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            html = r.text
            soup = BeautifulSoup(html, "html.parser")
            get_link(soup,index,indexlist)
    return index

def get_link(soup,index,indexlist):#, citylist, pagenum, headers):

    # for city in citylist:
    #     indexlist = {}
    #     number = pagenum[city] + 1
    #     for i in range(number)[1:]:
            # r = requests.get(url.format(city, i), headers=headers)
            # r.raise_for_status()
            # r.encoding = r.apparent_encoding
            # html = r.text
            # soup = BeautifulSoup(html, "html.parser")
    result_list = soup.find("div", {"class": "result_list"})
    sight_item_about = result_list.find_all("div", {"class": "sight_item_about"})
    sight_item_pop = result_list.find_all("div", {"class": "sight_item_pop"})

    for l,p in zip(sight_item_about, sight_item_pop):
        information = []
        title = l.find("a").get('title')
        try:
            level = l.find("span", {"class": "level"}).string
        except:
            level = "非A级景区"

        href = "piao.qunar.com" + l.find("a").get('href')  # 使用get获得标签中的属性内容
        # href：景点详情页的信息，level：景点的评级,title:景点名称，intro：景点的简介
        information.append(href)
        information.append(level)
        intro = l.find("div", {"class": "intro color999"}).get("title")
        information.append(intro)
        try:
            sales = p.find("span",{"class": "hot_num"}).string
        except:
            sales = "0"
        #sales = p.find("span", {"class": "hot_num"}).string
        information.append(sales)
        indexlist[title] = information
        index.append(indexlist)
    return index

cities = ["北京","上海", "成都", "三亚", "广州", "重庆", "深圳", "西安", "杭州", "厦门", "武汉", "大连", "苏州", "青岛", "天津", "南京", "香港", "桂林","郑州", "昆明"]

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87'}
url = "http://piao.qunar.com/ticket/list.htm?from=mpshouye_theme&keyword=必游景点&region={}&page={}"
pagenum = get_pagenum(cities, headers)
indexlist = download(url, cities, pagenum, headers)

with open("sight_link.json","r+",encoding="utf-8") as f:
    f.write(json.dumps(indexlist))
