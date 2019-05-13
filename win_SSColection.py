#!/usr/bin/python2.7
#coding=utf-8

import os,time
import socket

resultDict={}

def osTest():

    print "---System Checking---\n\r"
    import sysProcess
    sysProcess.process(resultDict)

def serviceTest():
    print "---Service Checking---\n\r"
    import serviceProcess
    serviceProcess.process(resultDict)

def userTest():
    print "---User Account Checking---\n\r"
    import userProcess
    userProcess.process(resultDict)

def pwdTest():
    print "---Password Security Checking---\n\r"
    import pwdProcess
    pwdProcess.process(resultDict)


def firewallTest():
    print "---Firewall Config Checking---\n\r"
    import firewallProcess
    firewallProcess.process(resultDict)


def fileTest():
    print "---File System Protection Checking---\n\r"
    import fileProcess
    fileProcess.process(resultDict)


def netTest():
    print "---Network Config Checking---\n\r"
    import netProcess
    netProcess.process(resultDict)

def saveResult(r):
    import json,time,sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    filename=time.strftime("%Y.%m.%d %H-%M-%S.dict", time.gmtime())
    t=json.dumps(r,ensure_ascii=False)
    f=open(filename,'wb')
    f.write(t)
    f.close()    

def shellThread():
    osTest()

    serviceTest()
    userTest()
    pwdTest()
    firewallTest()
    netTest()
    fileTest()

    resultDict["__type__"]='Windows'
    resultDict["__time__"]=time.strftime("%Y.%m.%d %H-%M-%S", time.gmtime())
    
    resultDict["IP"] = socket.gethostbyname(socket.gethostname())


    #saveResult(resultDict)    
    return resultDict
    
if __name__ == '__main__':
    shellThread()


    


    for i in resultDict.items():
        print i