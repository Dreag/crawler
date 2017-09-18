#coding=utf-8
import requests
import re
from bs4 import BeautifulSoup,Comment
from urllib.request import urlopen
#定义头部，防止爬虫被禁
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
			"Accept":"application/json, text/javascript, */*; q=0.01"}

#获取该页的网页源码
def getPage(url):
	r = requests.get(url,headers = headers)
	demo = r.text
	soup = BeautifulSoup(demo,"html.parser")
	#网页代码中的注释
	comments = soup.findAll(text=lambda text:isinstance(text, Comment))
	[comment.extract() for comment in comments]
	return soup

#获取帖子的主题，并将其写入字典test[post]中
def getPost(baseURL):
	r = requests.get(baseURL,headers = headers)
	#获取网页编码方式
	code = r.encoding
	if code.lower() != 'utf-8':
		r.encoding = 'gbk'		#编码为gb2312，非utf-8，转换成bgk
	demo = r.text
	soup = BeautifulSoup(demo,"html.parser")

	#正则匹配帖子的正文
	result = soup.find_all(id = re.compile("(postmessage|post_msg|content$)"))
	if result == []:
		result = soup.find_all(class_ = re.compile("content$"))
	#匹配post的时间
	time = soup.find_all(string = re.compile("^发表于|\d{4}-\d{2}-\d{2} ([01][0-9]|2[0-3]):[0-5][0-9]"))
	#获取标题
	title = soup.title.string
	#将帖子的标题写入到字典中
	test["post"]["title"] = title
	test["post"]["content"] = result[0].get_text().strip()
	test["post"]["publish_date"] = time[0]
	#写入源网页的replys
	startAppendDict(0,result,time,title)
	return title

#获取帖子的时间
def getTime(soup,result):
	#正则匹配标签中的关键字，返回列表
	time = soup.find_all(string = re.compile("^发表于|\d{4}-\d{2}-\d{2} ([01][0-9]|2[0-3]):[0-5][0-9]"))
	return time

#获取帖子页数
def getPageNum(url):
	try:
		rawtext = urlopen(url).read()
		soup = BeautifulSoup(rawtext,"html.parser")
		targetDiv=soup.find('div',{'class':'pg'})
		catalogLinks=targetDiv.find_all('a')
		indexlist = []
		for l in catalogLinks[1:]:
			indexlist.append(l.get('href'))
		#返回列表类型的帖子链接
		return indexlist
	except 	Exception as e:
		return None

#获取帖子的内容
def getPageContent(index):
	result = soup.find_all(id = re.compile("(postmessage|post_msg|content$|paragraph)"))
	if result == []:
		result = soup.find_all(class_ = re.compile("content$"))
	return result

#将回复贴添加到字典key：replys中
def startAppendDict(i,result,time,title):
	for texts in result[1:]:
		i += 1
		text = texts.get_text().strip()
		test["replys"].append({"content": text, "title": title, "publish_date": time[i]})

#文件存储
def store(measurements,title):
    import json
    with open('bbs_json/' + title + '.json', 'w',encoding = 'utf-8') as f:
        f.write(json.dumps(test))
    with open('verify_result.txt','a+') as f_txt:
    	f_txt.write(baseURL + str(test))

#读入测试网页链接
infile = open("bbs_urls2.txt","r")
bbs_urls = infile.readlines()
i = 0
for baseURL in bbs_urls:
	i += 1
	#测试字典
	test = {
	"post": {
		"content":"",
		"title":"",
		"publish_date":""
	},
	"replys": [
		]
	}
	try:
		title = getPost(baseURL)
		indexlist = getPageNum(baseURL)
				#print(len(indexlist))
		if indexlist != None: 
			for index in indexlist:
				soup = getPage(index)
				result = getPageContent(soup)
				time = getTime(soup,result)
				startAppendDict(-1,result,time,title)
		if __name__ == "__main__":
			store(test,title)
	except Exception as e:
		print(i)