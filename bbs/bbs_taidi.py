#coding=utf-8
import requests
import re
from bs4 import BeautifulSoup, Comment
from urllib.request import urlopen
	#定义头部，
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
			"Accept":"application/json, text/javascript, */*; q=0.01"}
	#去除img标签,7位长空格
removeImg = re.compile(r'<img.*?>| {7}|')
    #删除超链接标签
removeAddr = re.compile(r'<a.*?>|</a>')
    #把换行的标签换为\n
replaceLine = re.compile(r'<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
replaceTD= re.compile(r'<td>')
    #把段落开头换为\n加空两格
replacePara = re.compile(r'<p.*?>')
    #将换行符或双换行符替换为\n
replaceBR = re.compile(r'\r\n|\n')
    #将其余标签剔除
removeExtraTag = re.compile(r'<!--.*?-->')

#去除正则匹配的无用字符
def replace(x):
	x = re.sub(removeImg,"",x)
	x = re.sub(removeAddr,"",x)
	x = re.sub(replaceLine,"\n",x)
	x = re.sub(replaceTD,"\t",x)
	x = re.sub(replacePara,"",x)
	x = re.sub(replaceBR,"",x)
	x = re.sub(removeExtraTag,"",x)
    #strip()将前后多余内容删除
	return x.strip()

#获取该页的网页源码
def getPage(url):
	r = requests.get(url,headers = headers)
	demo = r.text
	soup = BeautifulSoup(demo,"html.parser")
	return soup

#获取主题帖的内容（包括title、content、time等）
def getPost(baseURL):
	r = requests.get(baseURL,headers = headers)
	#若编码非utf-8，转换成bgk
	code = r.encoding
	if code.lower() != 'utf-8':
		r.encoding = 'gbk'
	demo = r.text
	soup = BeautifulSoup(demo,"html.parser")
	#获取征文信息、得到提取结果result
	result = soup.find_all(id = re.compile("(postmessage|message|content$|^post_content|post_msg)"))
	#若通过id属性提取的result列表为空，则使用class属性提取
	if result == []:
		result = soup.find_all(class_ = re.compile("bbs-content|acticle_cont"))
	#通过正则提取时间标签中的字符串记为time，此时time为一个列表
	time = soup.find_all(string=re.compile(r"^发表于|\d{4}-\d{1,2}-\d{1,2} ([01][0-9]|2[0-3]):[0-5][0-9]?"))
	#获取标题
	title = soup.title.string
	#将标题和主帖写入到字典中
	Dict["post"]["title"] = title
	Dict["post"]["content"] = replace(result[0].get_text().strip())
	#筛选出time中字符串的时间YYYY-MM-DD并将其写入字典
	r_time = re.search(r"\d{4}.\d{1,2}.\d{1,2}",time[0])
	if r_time != None:
		Dict["post"]["publish_date"] = r_time.group(0)
	else:
		Dict["post"]["publish_date"] = time[0]
	#将baseurl中的回复帖写入字典
	AppendDict(0,result,time,title)
	return title

#获取时间
def getTime(soup):
	time = soup.find_all(string = re.compile(r"^发表于|\d{4}-\d{1,2}-\d{1,2} ([01][0-9]|2[0-3]):[0-5][0-9]"))
	return time

#获取帖子页码（前10页）链接
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

#获取回复帖内容
def getPageContent(index):
	#正则匹配标签中的关键字，返回列表
	result = soup.find_all(id = re.compile("(postmessage|message|post_msg|^post_content|content$)"))
	if result == []:
		result = soup.find_all(class_ = re.compile("bbs-content|acticle_cont"))
	return result

#将其导入到
def AppendDict(i,result,time,title):
	for texts in result[1:]:
		i += 1
		text = texts.get_text().strip()
		text = replace(text)
		#筛选出time中字符串的时间YYYY-MM-DD并将其写入字典
		r_time = re.search(r"\d{4}.\d{1,2}.\d{1,2}",time[i])
		Dict["replys"].append({"content": text, "title": title, "publish_date": r_time.group(0)})

#将字典写入到json文件和txt文件
def store(measurements,title):
    import json
    with open("/home/cherry963/PycharmProjects/Python/crawler/bbs/results/"+ title + '.json', 'w',encoding = 'utf-8') as f:
        f.write(json.dumps(Dict))
    with open('/home/cherry963/PycharmProjects/Python/crawler/bbs/verify_result.txt','w+') as f_txt:
    	f_txt.write("\n" + baseURL + str(Dict))

#读入测试网页
infile = open("/home/cherry963/PycharmProjects/Python/crawler/bbs/url_verify.txt","r")
bbs_urls = infile.readlines()
for baseURL in bbs_urls:
	#测试字典
	Dict = {
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
		if indexlist != None: 
			for index in indexlist:
				soup = getPage(index)
				result = getPageContent(soup)
				time = getTime(soup)
				AppendDict(-1,result,time,title)
		if __name__ == "__main__":
			store(Dict,title)
	except Exception as e:
		print("..")