#!/usr/bin/python2.7
#coding=utf-8
import os

def process(result):

    #默认共享检查
    r= os.system("net share >share.log")
    output=open("share.log",'r').readlines()
    try:
        result["File Share Resource"]=['  '.join(i.split()) for i in output[4:-2]]
    except:
        result["File Share Resource"]=''

    value = ''
    for item in output[4:-1]:
        value = item
        print(value)

    os.remove("share.log")

    return



if __name__ == '__main__':

    r={}
    process(r)
    print (r)
   