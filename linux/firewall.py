import os
import platform
import json
import re


def get_os_info():
    os_info = platform.uname()._asdict()
    return os_info


def process(result):
    info = {}
    result['info'] = info

    os_info = get_os_info()

    is_fw_run = False

    # 查看 iptables 服务
    os.system("systemctl list-units | grep iptables > firewall.txt")
    fw_service = open("firewall.txt", "r").readlines()
    info['Service iptables'] = fw_service
    if len(fw_service) > 0:
        is_fw_run = True

    # 查看 firewalld 服务
    os.system("systemctl list-units | grep firewalld > firewall.txt")
    fw_service = open("firewall.txt", "r").readlines()
    info['Service firewalld'] = fw_service
    if len(fw_service) > 0:
        is_fw_run = True

    if is_fw_run:
        result['risk_level'] = 0
        result['risk_desc'] = '系统防火墙正在运行中，可有效防范一些网络攻击。'
        result['solution'] = '无'
    else:
        result['risk_level'] = 3
        result['risk_desc'] = '系统防火墙未开启，有较大的安全风险。'
        result['solution'] = '请检查 firewalld 服务是否正常运行，如果没有安装防火墙，请先安装并启动防火墙；同时设置 firewalld 服务为开机启动。'

    os.remove('firewall.txt')


if __name__ == '__main__':
    _result = {}
    process(_result)

    print(_result)
