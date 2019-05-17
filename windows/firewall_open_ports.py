#!/usr/bin/python3.7
# coding=utf-8
import os
import json


def getValue(t):
    return t.split("=")[-1].strip()


def process(info):
    r = os.system("netsh firewall show state > firewall.log")
    line_array = open("firewall.log", 'r').readlines()

    # 命令执行，部分结果如下：

    # 操作模式 = 启用              (第4行)
    # 例外模式 = 启用
    # 多播 / 广播响应模式 = 禁用
    # 通知模式 = 禁用
    # 组策略版本 = Windows Defender 防火墙
    # 远程管理模式 = 禁用
    #
    # 所有网络接口上的端口当前均为打开状态:
    # 端口      协议      版本      程序        （第12行）
    # -------------------------------------------------------------------
    # 当前没有在所有网络接口上打开的端口。
    #
    # 重要信息: 已成功执行命令。
    start_index = 14
    port_state = getValue(line_array[start_index])
    if port_state.find("当前没有在所有网络接口上打开的端口") >= 0:
        info["Firewall All-Open Ports Exist"] = 'false'
        info["All-Open Ports List"] = []
    else:
        info["Firewall All-Open Ports Exist"] = 'true'
        end_index = start_index
        for index in range(start_index, len(line_array)):
            if line_array[index][0] == ' ':
                end_index = index
                break
        info["All-Open Ports List"] = [line.strip() for line in line_array[start_index: end_index]]

    os.remove('firewall.log')

    # 用于测试
    info["Firewall All-Open Ports Exist"] = 'true'
    info["All-Open Ports List"] = [
        "9019    UDP    任何    (null)\n",
        "8080    TCP    任何    (null)\n",
        "245     UDP    任何    (null)\n", ]

    return


def analyze(result):
    info = result['info']
    if info['Firewall All-Open Ports Exist'] == 'true':
        result['risk_level'] = 2
        result['risk_desc'] = '端口规则存在安全风险\n'
        result['risk_desc'] += '端口   协议  版本  程序\n'
        port_list = info["All-Open Ports List"]
        for index in range(0, len(port_list)):
            result['risk_desc'] += port_list[index]
        result['solution'] = '请检查防火墙的端口规则，对需要限制的端口运行设置命令：netsh firewall add/set portopening。'
    else:
        result['risk_level'] = 0
        result['risk_desc'] = '未发现无限制打开的端口。'
        result['solution'] = '无'

    return


if __name__ == '__main__':
    info = {}
    process(info)

    result = {'info': info}
    analyze(result)
    print(result)
