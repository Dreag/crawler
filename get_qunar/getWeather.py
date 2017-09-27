# -*- coding:utf-8 -*- 
import requests
import random
import time
import json
from bs4 import BeautifulSoup


# 获取网页源码
def getHtmlContent(url, headers):
    timeOut = random.choice(range(100, 180))  # 设置超时时间
    response = requests.get(url, headers=headers, timeout=timeOut)
    response.encoding = 'utf-8'  # 必须进行编码
    return response.text


# 通过源码获取天气信息
def getWeatherCondiction(webHtml):
    finalResult = []  # 最终输出的结果
    bs = BeautifulSoup(webHtml, "html.parser")  # 建立bs对象
    body = bs.body
    data = body.find("div", {"id": "7d"})  # 天气信息在<div id = "7d">中
    ul = data.find("ul")
    li = ul.find_all("li")
    # 对内容进行检索
    for day in li:
        temp = []
        date = day.find("h1").string  # 日期在li中的<h1>中
        temp.append(date)  # 将时间加入列表
        weather = day.find_all("p")[0].string
        temp.append(weather)  # 将天气情况加入列表
        span = day.find_all("p")[1].find("span")
        if span is None:  # 当晚上时，网站本天将不再有最高温度,，所以加一个判断
            temperatureHigh = ""
        else:
            temperatureHigh = span.string
        temp.append(temperatureHigh)
        temperatureLow = day.find_all("p")[1].find("i").string
        temp.append(temperatureLow)
        finalResult.append(temp)  # 将这天的天气信息加入到列表中
    return finalResult


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87'}

proxy = ["60.175.213.231:41239",
         "115.207.80.145:808",
         "58.19.63.181:808",
         "114.254.229.233:8118",
         "111.56.5.41:80",
         "61.153.67.110:9999",
         "60.178.169.4:8081"]

city_file = open("city.json", "r+", encoding="utf-8")
city_code = json.load(city_file)
all_cityweather = {}
for key, value in city_code.items():
    url = "http://www.weather.com.cn/weather/" + value + ".shtml"
    Result = getWeatherCondiction(getHtmlContent(url, headers))
    all_cityweather[key] = Result

with open("weather.json", "r+", encoding="utf-8") as f:
    f.write(json.dumps(all_cityweather))
