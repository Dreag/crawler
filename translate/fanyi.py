#coding=utf-8
import urllib.request
import urllib.parse
import json
import time
while True:
    
    content =input('请输入要翻译的内容：')
    
    if content =='q':
        break

    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=dict2.index'

    data={}
    data['type'] = 'AUTO'
    data['i'] = content
    data['doctype'] = 'json'
    data['xmlVersion'] = '1.8'
    data['keyfrom'] = 'fanyi.web'
    data['ue'] = 'utf-8'
    data['action'] = 'FY_BY_CLICKBUTTON'
    data['typoResult'] = 'true'

    headers = {}
    headers['User-Agent']='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'

    data = urllib.parse.urlencode(data).encode('utf-8')

    req = urllib.request.Request(url,data,headers)

    #req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36')

    response = urllib.request.urlopen(url,data)

    html = response.read().decode('utf-8')

    target = json.loads(html)

    print('翻译结果:%s'%(target['translateResult'][0][0]['tgt']))
    time.sleep(5)
