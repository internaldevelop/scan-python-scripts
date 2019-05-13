#!/usr/bin/python2.7
#coding=utf-8

import os,time,sys
#import paramiko
#import threading
import subprocess
import socket
#paramiko.util.log_to_file("paramiko.log")  

resultList=[]
class stdOUT:
    def __init__(self,output):
        self.output=output
        pass
    def readlines(self):
        return self.output

class Shell:
    def __init__(self):
        pass
    def exec_command2(self,cmd):
        obj=subprocess.Popen([cmd],bufsize=65536,stdout=subprocess.PIPE)
        output,error=obj.communicate()
        inputObj,outputObj,errorObj=stdOUT(cmd),stdOUT(output),stdOUT(error)
        return inputObj,outputObj,errorObj
    def exec_command(self,cmd):
        obj=os.popen(cmd)
        output=obj.readlines()
        error=''
        inputObj,outputObj,errorObj=stdOUT(cmd),stdOUT(output),stdOUT(error)
        return inputObj,outputObj,errorObj

    def close(self):
        pass


def saveResult(r,ip):
    import json,time,sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    filename=ip+time.strftime(" @%Y.%m.%d %H-%M-%S.dict", time.gmtime())
    t=json.dumps(r,ensure_ascii=False)
    f=open(filename,'wb')
    f.write(t)
    f.close()

def saveResult2(r):
    import json,time,sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    ip='localhost'    
    filename=ip+time.strftime(" @%Y.%m.%d %H-%M-%S.dict", time.gmtime())
    t=json.dumps(r,ensure_ascii=False)
    f=open(filename,'wb')
    f.write(t)
    f.close()

def shellThread():
    global resultList

    print "Begin......\n\r"

    rDict={}
    output=[]
    ssh=Shell()

    rDict['SSHObj']=ssh
    
    print "---System Checking---\n\r"
    import sysProcess
    sysProcess.process(rDict)
    rDict["__type__"]='Linux'
    rDict["__time__"]=time.strftime("%Y.%m.%d %H-%M-%S", time.gmtime())
    rDict["IP"] = socket.gethostbyname(socket.gethostname())
    
    ssh.close()
    
    resultList+=[rDict]

    rDict.pop("SSHObj")
    print "\r\nEnd......\r\n"    

    return rDict
    
    

def sshThread(ip,port,username,passwd):
    global resultList

    print ip,"Begin......\n\r"

    rDict={'ip':ip,'port':port,'username':username,'passwd':passwd}
    output=[]
    ssh=None
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(rDict['ip'],rDict['port'],rDict['username'],rDict['passwd'],timeout=5)
        print '%s\tOK\n'%(ip)

    except Exception,e:
        print 'ssh %s\tError. '%(ip),Exception,":",e
        return {}

    rDict['SSHObj']=ssh
    
    print ip,"---System Checking---\n\r"
    import sysProcess
    sysProcess.process(rDict)
    rDict["__type__"]='Linux'
    rDict["__time__"]=time.strftime("%Y.%m.%d %H-%M-%S", time.gmtime())
    rDict["IP"] = socket.gethostbyname(socket.gethostname())
    ssh.close()
    
    resultList+=[rDict]

    rDict.pop("SSHObj")
    saveResult(rDict,ip)
    
    print ip,"\r\nEnd......\r\n"
    

if __name__=='__main__':
    shellThread()
    #saveResult(resultList)
    '''
    for r in  resultList:
        print '-'*40
        for i in r.items():
            print i
    '''
    pass

