#!/usr/bin/python2.7
#coding=utf-8
import os
def getRegValue(lines):
    r=[]
    for i in lines:
        v=i.split("  REG_SZ  ")
        if len(v)==2:
            r+=[(v[0].strip(),v[1].strip())]

    return r


commonTaskList=['audiodg.exe', 'cmd.exe', 'conhost.exe','csrss.exe', 'dwm.exe', 'dllhost.exe', 'explorer.exe',
                'iexplore.exe','lsass.exe', 'lsm.exe','msdtc.exe', 'notepad.exe', 'python.exe','regedit.exe', 
                'System Idle Process', 'System', 'smss.exe',  'services.exe',  'svchost.exe', 'spoolsv.exe',
                'taskhost.exe', 'tasklist.exe','wininit.exe', 'WmiPrvSE.exe','winlogon.exe']
def getTasklist(lines):
    r=[]
    for i in lines[3:]:
        v=i.split("   ")
        if len(v)>1:
            if v[0] not in commonTaskList:
                r+=[v[0]]
    return r

def getServiceList(lines):
    r=[]
    for i in lines[2:-3]:
        r+=[i.strip()]
    return r


def process(result):

    #检查系统进程
    output = os.system("tasklist  >Service_task.log")
    result['Service Task List']=getTasklist(open("Service_task.log",'r').readlines())


    #检查系统服务
    output = os.system("net start >Service_service.log")
    result['Service Running List']=getServiceList(open("Service_service.log",'r').readlines())


    #检查开机启动项
    output = os.system("reg query HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run >Service_reg.log")
    result['Service AutoRun List']=getRegValue(open("Service_reg.log",'r').readlines())
    output = os.system("reg query HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run >Service_reg.log")
    result['Service AutoRun List']+=getRegValue(open("Service_reg.log",'r').readlines())

  
    return 

def processService(line):
    return line[3].split(":")[1].strip()


if __name__ == '__main__':

    r={}

    process(r)
    print r
   