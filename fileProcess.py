#!/usr/bin/python2.7
#coding=utf-8
import os

def getValue1(lines,key):
    r=''
    for i in lines:

        if key in i:
            r=i.split()[-1]
    return r
            
def getValue(lines,key):
    r=''
    for i in lines:
        v=i.split()
        if len(v) >2:
            if key == v[0]:
                r=v[-1]
    return r    

def process(result):

    #检查磁盘分区是否使用NTFS格式
    #'''
    r = os.system("chkdsk c: /i/c >disk.log")
    output=open("disk.log",'r').readlines()
    if "NTFS" in output[0]:
        result["File system type"]="NTFS"
    else:
        result["File system type"]=filter(str.isalnum, output[0].split()[-1])

    #检查磁盘分区可用空间是否不足
    result["File Available disk space"]=filter(str.isdigit, output[-5])+' KB'
    #'''

    #默认共享检查
    r= os.system("net share >share.log")
    output=open("share.log",'r').readlines()
    try:
        result["File Share Resource"]=['  '.join(i.split()) for i in output[4:-2]]
    except:
        result["File Share Resource"]=''

    #检查重要文件/目录
    r= os.system("reg query HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced\Folder\Hidden\SHOWALL\ >reg.log")
    output=open("reg.log",'r').readlines()
    result["File Hidden"]=getValue(output,"CheckedValue")

    #检查是否删除OS/2 和 POSIX 子系统
    r= os.system('reg query HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session" "Manager\SubSystems\ >reg.log')
    output=''.join(open("reg.log",'r').readlines())
    if "Posix" or "OS2"  in output:
        result["File OS2/Posix Subsystem"]="1"
    else:
        result["File OS2/Posix Subsystem"]="0"

    os.remove("disk.log")
    os.remove("share.log")
    os.remove("reg.log")

    return



if __name__ == '__main__':

    r={}
    process(r)
    print r
   