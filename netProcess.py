#!/usr/bin/python2.7
#coding=utf-8
import os

def getFromRegedit(log,key):
    for i in log:
        Parameters= i.split()
        if len(Parameters)==3 and key==Parameters[0]:
            return Parameters[-1]
    return '0'

def getFromNetstat(output):

    endline=0
    for i in output:
        if "  UDP  " in i:
            endline=output.index(i)
            break
    TcpConnections=output[4:endline]
    beginLine=0
    portList=[]
    for i in range(0,len(TcpConnections)):
        if '[' in TcpConnections[i] and "]" in TcpConnections[i]:
            
            if not " TCP " in TcpConnections[i-1]:
                exeName=TcpConnections[i-1].strip()+TcpConnections[i].strip()
                endline=i-1
            else:
                exeName=TcpConnections[i].strip()
                endline=i

            try:
                for pp in range(beginLine,endline):
                    flg,port,ip,state=TcpConnections[pp].split()
                    portList+=[(port.split(':')[-1],ip,exeName)]  
            except:
                pass

            beginLine=i+1

        elif "\xce\xde\xb7\xa8" in TcpConnections[i] or "Can not obtain" in TcpConnections[i]:
            exeName='Null'
            endline=i

            try:
                for pp in range(beginLine,endline):
                    flg,port,ip,state=TcpConnections[pp].split()
                    portList+=[(port.split(':')[-1],ip,exeName)]  
            except:
                pass

            beginLine=i+1
        else:
            pass
    return portList


def process(result):

    #检查网络通信TCP端口
    r = os.system("netstat -anb > netPort.log")
    output=open("netPort.log",'r').readlines()    
    result["Network TCP Port"]=getFromNetstat(output)

    #检查禁止响应ICMP重定向报文
    r= os.system('reg query HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters >Net_reg.log')
    result["Network ICMP Redirect"]=getFromRegedit(open('Net_reg.log','r').readlines(),'EnableICMPRedirect')


    os.remove("netPort.log")
    os.remove("Net_reg.log")


    return


if __name__ == '__main__':

    r={}
    process(r)


    for i in r["Network TCP Port"]:
        print i

    print r
   