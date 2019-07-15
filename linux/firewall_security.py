#!/usr/bin/python3.7
# coding=utf-8
import os
import json


# def ping_ip(ip):  # 1、ping指定IP判断主机是否存活
#     output = os.popen('ping -c 1 %s' % ip).readlines()  # 注：若在Linux系统下-n 改为 -c
#     for w in output:
#         if str(w).upper().find('TTL') >= 0:
#             # IPList.append(ip)
#             print(ip)


def getValue(t):
    return t.split("=")[-1].strip()


# def process(info):
def process(result):
    info = {}
    result['info'] = info
    result['risk_level'] = 0
    result['risk_desc'] = ''
    result['solution'] = '无'

    # ping_ip("127.0.0.1")

    # print(getValue("v= 100"))

    output = os.popen('systemctl status firewalld.service').readlines()  # 注：若在Linux系统下-n 改为 -c
    print(output)
    for w in output:
        if str(w).upper().find('ACTIVE: ACTIVE') >= 0: #Active: active (running)
            info['Firewall Operational mode'] = '启用'
            result['risk_level'] = 0
            result['risk_desc'] = '防火墙已正确开启'
            result['solution'] = '无'
        else:
            info['Firewall Operational mode'] = '未启用'
            result['risk_level'] = 3
            result['risk_desc'] = '防火墙未开启，系统不能有效保障网络安全，也不能对网络存取和访问进行有效的监控审计，系统和用户的信息资料有较大的外泄风险。'
            result['solution'] = '请使用命令开启防火墙：\n\tsystemctl start firewalld.service'



    return



if __name__ == '__main__':
    info = {}
    process(info)
    print(info)

    result = {'info': info}
    # analyze(result)
    # print(result)

    # result = oscoreversion()
    # print(result)
