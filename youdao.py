# -*- coding:utf-8
# TUDO:
# 1.scrapy
# 2.增加自定义释义
import cookielib
import sys
import urllib
import urllib2
import global_var
import re

def login():
    url = 'https://logindict.youdao.com/login/acc/login'
    filename = 'cookieyd.txt'
    cookie = cookielib.MozillaCookieJar(filename)
    global opener
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    postdata = urllib.urlencode({
        'app':'web',
        'tp':'urstoken',
        'cf':'3',
        'fr':'1',
        'product':'DICT',
        'type':'1',
        'um':'true',
        'username':'raybao2015@163.com',
        'password':'57afcd1926b82b03df1455a88c476c4e'
        })

    result = opener.open(url, postdata)
    cookie.save(ignore_discard = True, ignore_expires = True)

    #data = result.read()
   #print data
#TUDO using scrapy
def searchWD(word):
    url = 'http://dict.youdao.com/fsearch?q='+word+'&pos=-1&keyfrom=webwordbook&doctype=xml&xmlVersion=3.3'
    result = opener.open(url)
    result = result.read()
    #print result
    data1 = re.findall(u"<translation><content><\!\[CDATA\[(.*)\]\]><\/content>",result)
    data2 = re.findall(u"<us-phonetic\-symbol>(.*)<\/us-phonetic\-symbol>", result)
    #print data
    if data1 == [] or data2== []:
        return ['','']
    return ['\n'.join(data1),data2[0]]

def addword(word,phonetic,desc,tag):
    url = 'http://dict.youdao.com/wordbook/wordlist?action=add'
    header = {'Host':'dict.youdao.com',
              'User-Agent':	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
              'Content-Type':	'application/x-www-form-urlencoded',
              'Referer':'http://dict.youdao.com/wordbook/wordlist'
              }
    postdata = urllib.urlencode({
        'word':word,
        'phonetic':phonetic,
        'desc':desc,
        'tags':tag
        })
    print ">>>Add Word:\n" + word
    request = urllib2.Request(url,postdata,header)
    result = opener.open(request)
    
    
def addwords(words,tag):
    try:
        for word in words:
            res = searchWD(word)
            phonetic = res[1]
            desc = res[0]
            addword(word,phonetic,desc,tag)
    except:
        print  sys.exc_type,":",sys.exc_value
login()
tag = raw_input(">>>Input tag name: ")
fPath = global_var.WORD_PATH+tag+'.txt'

#addword('d','1','1','day1')
#addword('dad','1','1','')

#split whiteback
f = open(fPath,'r')
data=re.sub(' +|\\n+',',',f.read())
data = data.split(',')
while '' in data:
     data.remove('')

print "You are adding " + str(len(data))+'to ' + tag +' list!'
addwords(data,tag)

 
