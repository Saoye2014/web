# -*-coding:utf-8
import youdaoLib.youdao as ydLib
import sys
import re
import codecs

wordPath = '/Users/raybao/Desktop/单词/'
fPath = wordPath+'input.txt'
with codecs.open(fPath,'r',encoding = 'utf16') as f:
    data = re.sub('\n+','\n',f.read())
    data = data.encode('utf8')
data = data.split('\n')
formData = []
ydLib.login()
for row in data:
    if row == '':
        continue;
    if row[0] =='^':
        formData.append(row[1:len(row)]+'\t\n')
        print "add:"+row[1:len(row)]
    else:
        tmp = row.split(' ')
        while ''in tmp:
            tmp.remove('')
        for word in tmp:
            res = ydLib.searchWD(word)
            res[0] = re.sub('\n',';',res[0])
            w = word+'\t'+res[0]+'\n'
            print w
            formData.append(w);
            print "add:"+word
fPath = wordPath+'output.txt'
f2=open(fPath,'w')
f2.write(''.join(formData))
f2.close()
f.close()

