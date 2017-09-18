import itchat
import json
import jieba
import re
import PIL.Image as Image
import numpy as np
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from itchat.content import TEXT
from collections import Counter


# 带对象参数注册，对应消息对象将调用该方法
@itchat.msg_register(TEXT, isFriendChat=True, isGroupChat=True, isMpChat=True)
def text_reply(msg):
    msg.user.send('%s: %s' % (msg.type, msg.text))


# 好友性别比例
def friends_sex(friends):
    male = female = unknown = 0
    for friend in friends[1:]:
        sex = friend['Sex']
        if sex == 1:
            male += 1
        elif sex == 0:
            female += 1
        else:
            unknown += 1
    total = male + female + unknown
    print("male: {:d} %.2f%%".format(male) % (100 * float(male) / total))
    print("female: {:d} %.2f%%".format(female) % (100 * float(female) / total))
    print("unknown: {:d} %.2f%%".format(unknown) % (100 * float(unknown) / total))


# 好友地区分布
def friends_area(friends):
    provinces = []
    cities = []
    for friend in friends[1:]:
        provinces.append(friend['Province'])
        cities.append(friend['City'])
    province = dict(Counter(provinces))
    city = dict(Counter(cities))
    return province, city


# 好友个性签名signature
def friends_sign(friends):
    siglist = []
    for friend in friends:
        signature = friend['Signature'].strip().replace("span","").replace("class","").replace("emoji","")
        rep = re.compile("1f\d+\w*|[<>/=]")
        signature = rep.sub("",signature)
        siglist.append(signature)
    text = "".join(siglist)
    return text


# 将数据写入到文件中
def file_store(prov, city):
    with open("province.json", 'w+', encoding='utf-8') as f1:
        f1.write(json.dumps(prov))
    with open("city.json", 'w+', encoding='utf-8') as f2:
        f2.write(json.dumps(city))


# 制作词云图
def plot_yun(text):
    wordlist = jieba.cut(text, cut_all=True)
    wl_space_split = " ".join(wordlist)
    coloring = np.array(Image.open("wechat.jpg"))
    wordcloud = WordCloud(background_color="white",max_words=2000,mask=coloring, max_font_size=60, random_state=42, scale=2, font_path="simhei.ttf").generate(wl_space_split)
    image_color = ImageColorGenerator(coloring)
    plt.imshow(wordcloud.recolor(color_func=image_color))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()


if __name__ == '__main__':
    # 传入True hotReload使得程序关闭后一定时间内也可以登录，该方法会生成一个静态文件itchat.pkl，用于存储登陆的状态
    itchat.auto_login(hotReload=True)
    # 运用get_friends方法获得完整好友列表
    flist = itchat.get_friends(update=True)
    with open("wechat.json", 'w+', encoding='utf-8') as f:
        f.write(json.dumps(flist))

    friends_sex(flist)
    province, city = friends_area(flist)
    signature = friends_sign(flist)
    file_store(province, city)
    plot_yun(signature)
