#coding=utf-8  
import os
from bs4 import BeautifulSoup
import re
import urllib2
def html(url):  
    #html='http://www.weather.com.cn/weather/101010100.shtml' 
    html='http://www.weather.com.cn/weather1d/101180101.shtml' 
    headers = {'User-Agent':'Mozilla/5.0 (X11; U; Linux i686)Gecko/20071127 Firefox/2.0.0.11'}  
    req = urllib2.Request(url,headers=headers)  
    response = urllib2.urlopen(req).read()  
    soup = BeautifulSoup(response, 'html.parser')    
    city=[]  
    city.append(str(soup.title))  
    link= str(city).decode('string_escape')  
    pattern = re.findall(r'<title>(.*?)</title>',link)  
    title = str(pattern)  
    title_list = title[2:146]  
    print (str(title_list).decode('string_escape').decode("utf-8"))     
    href_list =[]  
    for link in soup.find_all(id="hidden_title"):            
        href_list.append(str(link))  
    pattern2 = re.compile(r'<.*? value="(.*?)"/>')  
    for href in href_list:       
        result = re.match(pattern2,href)  
        if result:  
            link_href=result.groups()[0]             
            print "%s " %link_href.decode("utf-8")  
    href_lis=[]  
    for link in soup.find_all('p'):  
        href_lis.append(str(link))  
    pattern3 = re.compile(r'<p class=".*?" title="(.*?)">.*?</p>')  
    result = re.match(pattern3,href_lis[0])  
    if result:  
            link_href=result.groups()[0]             
            print "%s " %link_href.decode("utf-8")  
    href_wind=[]  
    for link in soup.find_all('p'):  
        href_wind.append(str(link))  
    pattern4= (re.findall(r'<i>(.*?)</i>',href_wind[2]))  
    #print "风力：~{0}~".format(pattern4[1]).decode("utf-8")  
    print "内容来自：".decode("utf-8"),html  
html('http://www.weather.com.cn/weather1d/101180101.shtml')  
os.system('pause')  