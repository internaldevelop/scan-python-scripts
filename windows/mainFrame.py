#!/usr/bin/python2.7
#coding=utf-8


from windows import usbDog, win_SSColection as Colection
import codecs

def ReadFile(filePath,encoding="utf-8"):
    with codecs.open(filePath,"r",encoding) as f:
        return f.read()
 
def WriteFile(filePath,u,encoding="gbk"):
    with codecs.open(filePath,"w",encoding) as f:
        f.write(u)

def GBK_2_UTF8(src,dst):
    content = ReadFile(src,encoding="gb18030")
    WriteFile(dst,content,encoding="utf-8")


def saveResult(r):
    import json,time,sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    ip=r['IP']
    filename=ip+time.strftime(" @%Y.%m.%d %H-%M-%S.dict", time.gmtime())
    t=json.dumps(r,ensure_ascii=False)

    f=open(filename,'w')
    f.write(t)
    f.close()

    GBK_2_UTF8(filename,"UTF8_"+filename)


if __name__=='__main__':
    if usbDog.checkAuthority() or 1:
        
        rDict=Colection.shellThread()
        saveResult(rDict)
    else:
        pass


