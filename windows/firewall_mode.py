#!/usr/bin/python3.7
# coding=utf-8
import os


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
    info["Firewall Operational mode"] = getValue(line_array[4])
    info["Firewall Exception mode"] = getValue(line_array[5])
    info["Firewall Multi/Broadcast mode"] = getValue(line_array[6])
    info["Firewall Notification mode"] = getValue(line_array[7])

    os.remove('firewall.log')

    return


def analyze(result):
    info = result['info']
    if info['Firewall Operational mode'] != '启用':
        result['risk_level'] = 3
        result['risk_desc'] = '防火墙未开启，系统不能有效保障网络安全，也不能对网络存取和访问进行有效的监控审计，系统和用户的信息资料有较大的外泄风险。'
        result['solution'] = '请使用如下Windows命令开启防火墙：\n\tnetsh firewall set opmode mode=enable'
    elif result['Firewall Notification mode'] != '启用':
        result['risk_level'] = 1
        result['risk_desc'] = '防火墙未开启通知模式，在阻止应用访问网络时，可能会给用户带来困扰；同时，开启通知模式也有利于用户了解当前系统可能存在的安全隐患。'
        result['solution'] = '请使用如下Windows命令开启防火墙：\n\tnetsh firewall set notifications enable'
    else:
        result['risk_level'] = 0
        result['risk_desc'] = '防火墙已正确开启'
        result['solution'] = '无'

    return


if __name__ == '__main__':
    info = {}
    process(info)

    result = {'info', info}
    analyze(result)
    print(result)
