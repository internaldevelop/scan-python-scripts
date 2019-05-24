#!/usr/bin/python3.7
# coding=utf-8
import os
import re


def process(result):
    info = []
    result['info'] = info
    result['risk_level'] = 0
    result['risk_desc'] = '未发现网络端口问题。'
    result['solution'] = '无'

    # 检查网络通信TCP端口
    r = os.system("netstat -an -p TCP > netPort.log")
    output = open("netPort.log", 'r').readlines()

    # 解析每条TCP连接的信息
    close_wait_count = 0
    for index in range(4, len(output)):
        # 提取行信息到数组中
        # re.split(r'\s+', output[index])也可实现同样效果
        line = re.sub(' +', ' ', output[index].strip('\n'))
        item = line.split(' ')
        connect_info = {
            'protocol': item[1],
            'local_ip': item[2],
            'remote_ip': item[3],
            'status': item[4],
        }
        info.append(connect_info)
        # 保存 CLOSE_WAIT 状态的连接数
        if item[4] == 'CLOSE_WAIT':
            close_wait_count += 1

    # 检查是否有过多的 CLOSE_WAIT 连接，以50为阈值
    if close_wait_count > 50:
        result['risk_level'] = 1
        result['risk_desc'] = '大量端口（共计{}个）处于CLOSE_WAIT状态，有可能恶意程序在消耗本系统的资源。'.format(close_wait_count)
        result['solution'] = '设置注册表项 HKLM\System\CurrentControlSet\Services\Tcpip\Parameters下的键值：KeepAliveTime < ' \
                             '300000，以使被动关闭的端口能尽早释放出来。 '

    os.remove("netPort.log")

    return


if __name__ == '__main__':
    _result = {}
    process(_result)

    print(_result)
