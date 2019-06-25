#!/usr/bin/python3
# coding=utf-8
import os
import platform
import json


def get_os_info():
    os_info = platform.uname()._asdict()
    return os_info


def process(result):
    info = {}
    result['info'] = info

    os_info = get_os_info()

    # 获取root账户SSH远程登录限制的配置
    os.system("grep '^PermitRootLogin' /etc/ssh/sshd_config > root.txt")
    permit = open("root.txt", "r").readlines()

    # 如果读取不到 PermitRootLogin 开头的行，说明配置文件中这行被注释了
    # 按照 PermitRootLogin yes 做错误处理
    if len(permit) == 0:
        info['PermitRootLogin'] = "Not configured"
        split_permit = ["PermitRootLogin", "yes"]
    else:
        info['PermitRootLogin'] = permit[0]
        # 分割
        split_permit = permit[0].split()

    # 判断是否允许root远程登录
    if split_permit[1] == "yes":
        result['risk_level'] = 2
        result['risk_desc'] = '系统未限制root账户远程登录。'
        result['solution'] = '修改/etc/ssh/sshd_config文件，将PermitRootLogin yes改为PermitRootLogin no，重启sshd服务。'
    else:
        result['risk_level'] = 0
        result['risk_desc'] = '系统已限制root账户远程登录。'
        result['solution'] = '无'

    os.remove("root.txt")


if __name__ == '__main__':
    _result = {}
    process(_result)

    print(_result)
