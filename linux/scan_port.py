#!/usr/bin/python3
# -*- coding: utf-8 -*-
from socket import *


def process(result):
    info = []
    result['info'] = info
    result['risk_level'] = 0
    result['risk_desc'] = '未发现网络端口问题。'
    result['solution'] = '无'

    openportcount = 0
    ip = '127.0.0.1'

    setdefaulttimeout(1)
    for p in range(1, 65536):
        try:
            s = socket(AF_INET, SOCK_STREAM)
            s.connect(('127.0.0.1', p))
            print('[+] %d open' % p)
            s.close()

            openportcount += 1
            port_info = {
                # 'local_ip': ip,
                'port': p,
                'status': 'open',
            }
            info.append(port_info)

        except:
            pass


    # 开放端口大于3时，需检查确认是否有多余端口
    if openportcount > 3:
        result['risk_level'] = 1
        result['risk_desc'] = '系统开放了太多端口，存在安全风险 共计开放{}个端口。'.format(openportcount)
        result['solution'] = '请联系系统管理员，维护与工作无关的端口'
    else:
        result['risk_level'] = 0
        result['risk_desc'] = '开放端口数量处于正常范围'
        result['solution'] = '无'


if __name__ == '__main__':
    _result = {}
    process(_result)

    print(_result)
