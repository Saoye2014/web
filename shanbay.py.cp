 # -*- coding:utf-8
import gzip
import re
import cookielib
import urllib2
import urllib
import sys

wordlist = {}
wordbook = {}

def ungzip(data):
    try:        # 尝试解压
        print('正在解压.....')
        data = gzip.decompress(data)
        print('解压完毕!')
    except:
        print('未经压缩, 无需解压')
    return data

def getTOKEN(data):
    cer = re.compile('name=\'csrfmiddlewaretoken\' value=\'(.*)\'', flags = 0)
    strlist = cer.findall(data)
    return strlist[0]

def loginShanby():
    url = 'http://shanbay.com/accounts/login/'
    filename = 'cookie.txt'
    #声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
    cookie = cookielib.MozillaCookieJar(filename)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    op = opener.open(url)
    data = op.read()
    data = ungzip(data)     # 解压

    try:
        _token = getTOKEN(data)
        print _token
    except:
        print "get token error!", sys.exc_type, ":", sys.exc_value
        
    postdata = urllib.urlencode({
        'csrfmiddlewaretoken':_token,
	'username':'834926882@qq.com',
	'password':'12w3456',
        'token':'',
    })
    #模拟登录，并把cookie保存到变量
    result = opener.open(url,postdata)
    
    #保存cookie到cookie.txt中
    cookie.save(ignore_discard=True, ignore_expires=True)
    #利用cookie请求访问另一个网址，此网址是成绩查询网址
    #请求访问成绩查询网址
    data = result.read()
    print data
    if data.find('我的词库')!= -1:
        print "login sucess!"
        return opener
    else:
        print "login failes!"
        if data.find('验证码')!=-1:
            modelvalue = re.compile('name=\".*value=\"(.*)\".*src=\"(.*)\"')
            yzm = modelvalue.findall(data.decode('utf8'))
            for x in yzm:
                print x
            #TODOxianshi yzm 按顺序提取所有的key,value。选择自己想要的
            answer = raw_input("输入验证码：")
            postdata = urllib.urlencode({
                'csrfmiddlewaretoken':_token,
	        'username':'834926882@qq.com',
	        'password':'12w3456',
                'captcha_0':yzm[2],
                'captcha_1':answer
                })
            result = opener.open(url,postdata)
            cookie.save(ignore_discard=True, ignore_expires=True)
            data = result.read()
            print data
            if data.find('我的词库')!= -1:
                print "login sucess!"
                return opener
        
        print "unknown reason!"
        
        

def addWordList(opener):
    while 1:
        try:
            wordbook_id = 139210
            name = raw_input("input wordlist name:")
            desp = raw_input("input wordlist description:")
            wordlist_id = raw_input("input wordlist_id(default 0: "+str(wordbook_id)+"):")
            if wordbook_id!=0:
                wordbook_id = 139210
            break
        except KeyboardInterrupt :
            sys.exit(0)
            break
        except:
            print "please input again:",sys.exc_type,":",sys.exc_value
    
    postdata = urllib.urlencode({
        'name':name,
        'description':desp,
        'wordbook_id' : wordbook_id,
        })

    url = 'http://www.shanbay.com/api/v1/wordbook/wordlist/'
    result = opener.open(url,postdata)

oppSets = {0:loginShanby, 1:addWordList}
opener = oppSets[0]()
opp = input("Your opp:")
while opp != -1:
    if opp==0:
        opener = oppSets[opp]()
    if opp == 1:
        try:
            oppSets[opp](opener)
        except:
            print(oppSets[1].func_name), sys.exc_type,":",sys.exc_value
    opp = input("Your opp:")

  
