#!/usr/bin/python2.7
#coding=utf-8
import os

def getValue(t):
    return t.split("=")[-1].strip()

def process(result):

    r = os.system("netsh firewall show state > firewall.log")
    output=open("firewall.log",'r').readlines()

    result["Firewall Operational mode"]=getValue(output[4])
    result["Firewall Exception mode"]=getValue(output[5])
    result["Firewall Multi/Broadcast mode"]=getValue(output[6])
    result["Firewall Notification mode"]=getValue(output[7])
    
    os.remove('firewall.log')
    
    return



if __name__ == '__main__':

    r={}
    process(r)
    print r
   