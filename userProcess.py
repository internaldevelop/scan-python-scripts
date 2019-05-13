#!/usr/bin/python2.7
#coding=utf-8
import os

def getAdmin(line):
    return [i.strip() for i in line[6:-2]]

def getUser(line):
    result=[]
    for i in line[4:-2]:
        result+=i.split()
    return result

def getValue(lines,key):
    r=''
    for i in lines:
        v=i.split()
        if len(v) >2:
            if key == v[0]:
                r=v[-1]
    return r

def process(result):

    #检查管理员权限账户
    output = os.system("net localgroup administrators >Account_admin.log")
    result['Account Admin']=getAdmin(open("Account_admin.log",'r').readlines())
    
    #检查所有账户
    output = os.system("net user >Account_user.log")
    result['Account Users']=getUser(open("Account_user.log",'r').readlines())
    for i in result['Account Users']:
        output = os.system("net user %s >>Account_Info.log"%i)
    line=open("Account_Info.log",'r').readlines()
    num=len(result['Account Users'])

    #检查账户启用情况
    result['Account Active']=[(result['Account Users'][i],line[5+i*26].split('  ')[-1].strip()) for i in range(num)]

    #检查账户是否需要密码
    result['Account Password Required']=[(result['Account Users'][i],line[11+i*26].split('  ')[-1].strip()) for i in range(num)]
    
    #检查上一次设置密码时间
    result['Account Password Last set']=[(result['Account Users'][i],line[8+i*26].split('  ')[-1].strip()) for i in range(num)]
    

    #检查是否禁止匿名用户空链接
    r= os.system("reg query HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Lsa\ >reg.log")
    result["Account Restrict Anonymous"]=getValue(open("reg.log",'r').readlines(),"restrictanonymous")

    #检查是否开启自动登录
    r= os.system('reg query HKEY_LOCAL_MACHINE\Software\Microsoft\Windows" "NT\CurrentVersion\Winlogon\ >reg.log')
    result["Account AutoAdminLogon"]=getValue(open("reg.log",'r').readlines(),"AutoAdminLogon")

    os.remove('Account_admin.log')
    os.remove('Account_user.log')
    os.remove('Account_Info.log')
    os.remove("reg.log")



    return 




if __name__ == '__main__':

    r={}
    process(r)
    print r
   