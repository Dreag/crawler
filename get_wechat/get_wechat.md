# 我的微信好友
前一段时间偶然间发现了itchat这个库，抽个时间用这个库来分析分析我的微信好友的情况。

---
itchat是一个开源的微信个人接口，目前支持Python2.7和Python3.5.
itchat已经上传到PyPi，使用pip即可安装
```python
pip install itchat
```
这里是itchat的GitHub地址——<a href="https://github.com/littlecodersh/ItChat">itchat</a>
这里是itchat的项目简介——<a href="http://itchat.readthedocs.io/zh/latest/">itchat项目简介</a>

_ _ _

### 1. 登录并获取全部好友信息
使用auto_login扫描二维码即可登录，传入True hotReload使得程序关闭后一定时间内也可以登录，该方法会生成一个静态文件itchat.pkl，用于存储登陆的状态
```python
if __name__ == '__main__':
	# 传入True hotReload使得程序关闭后一定时间内也可以登录，该方法会生一个静态文件itchat.pkl，用于存储登陆的状态
    itchat.auto_login(hotReload=True)
    # 运用get_friends方法获得完整好友列表
    flist = itchat.get_friends(update=True)
    #将数据保存到wechat.json文件中
    with open("wechat.json", 'w+', encoding='utf-8') as f:
        f.write(json.dumps(flist))
```
要注意的是得到的friends列表的第一个元素是用户本身的信息
### 2.获取性别信息
得到上面的friends数据之后，遍历列表中的每一个元素，每一个元素的类型都是字典。取出字典中的Sex关键字对应的word，男性为1，女性为0.
###### 统计结束之后，发现了一个令人悲伤的事情：
```JavaScript
男性: 191 67.49%
女性: 38  13.43%
未知: 54  19.08%
```

### 3.获取地区信息
同样的从上面得到的friends列表中即可得到好友所在省、城市的信息。利用第三方库collections进行统计每个返回列表中的重复项目及个数,返回类型为Counter类型，dict一下得到字典类型.
```python
# 好友地区分布
def friends_area(friends):
    provinces = []
    cities = []
    provinces.append([friend['Province'] for friend in friends[1:]])
    cities.append([friend['City'] for friend in friends[1:]])
    province = dict(Counter(provinces))
    city = dict(Counter(cities))
    return province, city
```

###### 省份分布情况
![](http://123.206.47.24/wp-content/uploads/2017/09/province-1.jpg)
###### 城市分布情况
![](http://123.206.47.24/wp-content/uploads/2017/09/city.jpg)

###### 因为我老家是在安徽阜阳，所以好友大都分布在河南和安徽两个省份，不过好多人都没有设置自己的性别和地区，这个也给统计造成了一定的误差。
### 4.制作个性签名词云
获得签名数据同上，friends['Signature'].
制作词云需要用到wordcloud,使用方法在GiuHub上都有，地址在这里(<a href="https://github.com/amueller/word_cloud">wordcloud</a>)
还需要一个分词组件，这里使用的是jieba分词，<a href="https://github.com/fxsjy/jieba">GitHub地址在这里</a>
注意在制作分词的时候，wordcloud默认字体没有中文，要自定义字体格式，从网上随便下个中文字体就可以了.
```python
def plot_yun(text):
    wordlist = jieba.cut(text, cut_all=True)
    wl_space_split = " ".join(wordlist)
    coloring = np.array(Image.open("wechat.jpg"))
    wordcloud = WordCloud(background_color="white",max_words=2000,mask=co
    loring, max_font_size=60, random_state=42, scale=2, font_path="simhei.ttf").generate(wl_space_split)
    image_color = ImageColorGenerator(coloring)
    plt.imshow(wordcloud.recolor(color_func=image_color))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
```
###### 得到的词云图是这个样子的,使用的样式是微信的图标
![](http://123.206.47.24/wp-content/uploads/2017/09/cloud_wechat.png)
##### too young，too simple.