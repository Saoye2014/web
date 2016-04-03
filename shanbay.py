 # -*- coding:utf-8
 #TUDO LIST
 #1.改掉opener
import gzip
import re
import cookielib
import urllib2
import urllib
import sys
import csv
ABC={'w':['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M'],'pos':0}
import global_var
def _print(s):
    print(">>>"+s)
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
    url = global_var.URL_SB_LOGIN
    filename = 'cookie.txt'
    #声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
    cookie = cookielib.MozillaCookieJar(filename)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    op = opener.open(url)
    data = op.read()
    data = ungzip(data)     # 解压
    ###print data
    try:
        _token = getTOKEN(data)
        print _token
    except:
        print "get token error!", sys.exc_type, ":", sys.exc_value
        
    postdata = urllib.urlencode({
        'csrfmiddlewaretoken':_token,
	'username':'834926882@qq.com',
	'password':'12w3456'
    })
    #模拟登录，并把cookie保存到变量
    result = opener.open(url, postdata)
    #print result
    #保存cookie到cookie.txt中
    cookie.save(ignore_discard=True, ignore_expires=True)
    #利用cookie请求访问另一个网址，此网址是成绩查询网址
    #请求访问成绩查询网址
    data = result.read()
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
            answer = raw_input(">>>XS输入验证码：")
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
    
        print ">>>Unknown reason!"

def getAllWB(opener):
    print "get all wordbook!"
    url = global_var.URL_SB_WB
    result = opener.open(url)
    data = result.read().decode('utf8')
   # print data
    m = re.findall(u"\/wordbook\/(?P<wb_id>\d+)\/\">(?P<wb_name>\w+[\u4e00-\u9fa5]*)<\/a>",data)

    if m == []:
        print ">>>Get empty"
        return
    s={}
    for pair in m:
       # print pair[1]
        s[pair[0]]=pair[1]

    print s
    return s
#TUDO
#def getAllList(openner,wbId):
def _addword(word,listID,opener):
    _print("Add: " + word)
    url = global_var.URL_SB_WD
    postdata = urllib.urlencode({
        'id':listID,
        'word': word
        })
    result = opener.open(url,postdata)
    s=eval(result.read())
    return s
            

def addwords(words, listID,listName,opener,op):
    mount = len(words)
    count  = 0
    for word in words:
        _print(op+": add "+str(count) + " of " + str(mount))
        while True:
            res = _addword(word, listID, opener)
            if(res["status_code"]==1):
                rtn=re.findall('\u4e0a',res["msg"])
                if rtn!=[]:
                    print ">>>词数达到上限"
                    dsp="ss"
                    wbID = 139210
                    rtn=_addWdList(listName,dsp,wbID,opener)
                    if rtn != 0:
                        listID = rtn
                        ABC['pos']=0
                        _print(op+": 新增列表："+str(listID))
                        
                elif (re.findall('10',res["msg"])!=[]):
                    if ABC['pos'] >= len(ABC['w']):
                        print ">>>ABC数组溢出"
                        dsp="ss"
                        wbID = 139210
                        rtn=_addWdList(listName,dsp,wbID,opener)
                        if rtn != 0:
                            listID = rtn
                            ABC['pos']=0
                            _print(op+": 新增列表："+str(listID))
                        else :
                            continue
                    _addword(ABC['w'][ABC['pos']],listID,opener)
                    ABC['pos']+=1
                else:
                    _print(op+" :Maybe done, the word aready exist or not be found or ....")
                    break

            else:
                _print(op+" :done!")
                count+=1
                break

def _addWdList(name,desp,wbID,opener):
    postdata = urllib.urlencode({
        'name':name,
        'description':desp,
        'wordbook_id' : wbID,
        })

    url = global_var.URL_SB_ADD_WL
    result = opener.open(url,postdata)
    rtn = eval(result.read())
    if rtn["status_code"]==0:
        listID = rtn["data"]["wordlist"]["id"] 
        return listID
    else:
        return -1
    
def addWordList(opener,op):
    while 1:
        try:
            wordbook_id = 139210	
            name = raw_input(">>>Input wordlist name:")
            desp = raw_input(">>>Input wordlist description:")
            wordlist_id = raw_input(">>>Input wordlist_id(default 0: "+str(wordbook_id)+"):")
            if wordbook_id!=0:
                wordbook_id = 139210
            
            rtn = _addWdList(name,desp,wordbook_id,opener)
            if rtn != -1:
                _print(op+":Success！")
                _print("新增列表："+str(rtn))
            else:
                _print(op+":Fail!")
            break
        except KeyboardInterrupt :
            sys.exit(0)
            break
        except:
            print ">>>Please input again:",sys.exc_type,":",sys.exc_value


0
oppSets = {0:loginShanby, 1:addWordList, 2:getAllWB, 3:addwords}
global_var.OPENER = oppSets[0]()

for k in global_var.OPCODE:
    print str(k)+": "+global_var.OPCODE[k],

print '\n'
opp = input("Your opp:")
while opp != -1:
    try:
        if opp == 0 :
            global_var.OPENER=oppSets[opp]();
        if opp == 1:
            oppSets[opp](global_var.OPENER, global_var.OPCODE[opp])
        if opp == 2:
            global_var.WORDBOOK = oppSets[opp](global_var.OPENER);
            for key in global_var.WORDBOOK.keys():
                print key.encode('utf8') +' '+ global_var.WORDBOOK[key].encode('utf8')
        if opp == 3:
            name = raw_input('>>>input the name of import file:')
            p = global_var.WORD_PATH+name+'.txt'
            f = open(p,'r')
            data=re.sub(' +|\\n+',',',f.read())
            data = data.split(',')
            while '' in data:
                data.remove('')
            listID = input(">>>Input list ID:")
            oppSets[opp](data, listID,name,global_var.OPENER,global_var.OPCODE[opp])
            
    except:
        print(oppSets[1].func_name), sys.exc_type,":",sys.exc_value
        
            
    opp = input("Your opp:")

  
