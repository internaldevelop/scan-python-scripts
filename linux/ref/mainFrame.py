#!/usr/bin/python2.7
#coding=utf-8
import linux_shell_Colection as Colection
#import usbDog



def saveResult(r):
    import json,time,sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    ip=r['IP']
    filename=ip+time.strftime(" @%Y.%m.%d %H-%M-%S.dict", time.gmtime())
    t=json.dumps(r,ensure_ascii=False)
    f=open(filename,'wb')
    f.write(t)
    f.close()


if __name__=='__main__':
    #if usbDog.checkAuthority():
    if 1：
        rDict=Colection.shellThread()
        saveResult(rDict)
    else:
        pass


