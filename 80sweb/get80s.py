import bs4
import requests
from bs4 import BeautifulSoup

#获取、解析网页
def getHTMLText(url):
	try:
		r = requests.get(url)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return ""

#获取网页内排名内容
def ranking(indexlist,html):
	soup = BeautifulSoup(html,"html.parser")
	target = soup.find('ul',{"class":"me1 clearfix"})
	results = target.find_all("li")
	for l in results:
		title = l.find("a").get('title')
		href = "www.80s.tw" + l.find("a").get('href')		#使用get获得标签中的属性内容
		indexlist[title] = href

# 将数据保存到
def save(indexlist):
	import json
	with open("80s.json",'w',encoding = 'utf-8') as f:
		f.write(json.dumps(indexlist))

def Print(indexlist):
	#tplt = "{0:^10}\t{1:{3}^15}\t{10:^20}"
	print("排名			"+"电影				"+"链接")
	i = 0
	for key in indexlist:
		i = i+1
		print(i,"  ",str(key),str(indexlist[key]))


def main():
	indexlist = {}
	for i in range(3):
		url = "http://www.80s.tw/movie/list/----h-p" + str(i)
		html = getHTMLText(url)
		ranking(indexlist,html)
		save(indexlist)
	Print(indexlist)
main()
