#!/usr/bin/python3.7
# coding=utf-8
import os
import json


def getValue(t):
    return t.split("=")[-1].strip()


def process(result):
    info = {}
    result['info'] = info
    result['risk_level'] = 0

    output = os.popen('cat /etc/bashrc').readlines()
    print(output)
    bsafety = False
    for w in output:
        if str(w).upper().find('EXPORT HISTTIMEFORMAT=') >= 0:
            bsafety = True

    if(bsafety):
        info['history timestamp'] = '启用'
        result['risk_level'] = 0
        result['risk_desc'] = '设置history时间戳已开启'
        result['solution'] = '无'
    else:
        info['history timestamp'] = '未启用'
        result['risk_level'] = 1
        result['risk_desc'] = 'history时间戳未设置'
        result['solution'] = '参考配置操作：在/etc/bashrc文件中增加如下行：export HISTTIMEFORMAT="%F %T"'



if __name__ == '__main__':
    info = {}
    process(info)
    print(info)
