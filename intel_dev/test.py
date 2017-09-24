import requests
import re
import json
from bs4 import BeautifulSoup

url = "https://software.intel.com/en-us/vtune-amplifier-help-building-and-installing-the-sampling-drivers-for-linux-targets"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87'}


r = requests.get(url,headers=headers)
html = r.text
soup = BeautifulSoup(html,"html.parser")
menu = soup.find("div",{"id":"block-book-navigation"})
big_title = menu.find_all("li",id=re.compile("dhtml_menu"))
all_link = {}
for i in big_title:
    link = []
    menu_title = i.find("a",{"class":"menu__link"}).string
    menu_link = i.find("a",{"class":"menu__link"}).get("href")
    link.append(menu_link)
    for lower_menu in i.find_all("a",{"class":"menu__link menu-node-unpublished menu-node-unpublished menu-node-unpublished menu-node-unpublished menu-node-unpublished menu-node-unpublished"}):
        lower_menu_dict = {}
        lower_menu_title = lower_menu.string
        lower_menu_link = lower_menu.get("href")
        lower_menu_dict[lower_menu_title] = lower_menu_link
        r = requests.get("https://software.intel.com"+lower_menu_link, headers=headers)
        html = r.text
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find("div", {"class": "book-page-content  hasFirstSidebar"})
        text = content.get_text()
        with open("file/" + lower_menu_title + ".txt","w+", encoding="utf-8") as f:
            f.write(text)
        link.append(lower_menu_dict)

    all_link[menu_title] = link

with open("test.json", "w+", encoding="utf-8") as f:
     f.write(json.dumps(all_link))
