#!/usr/bin/python3.7
# coding=utf-8
import os
import json


def getValue(t):
    return t.split("=")[-1].strip()


def getSSHPort(sshinfo):
    # // Examples:
    # // tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      11586/sshd
    split_ssh = sshinfo[0].split()
    # print(split_ssh[3])
    port = split_ssh[3].split(":")
    # print(port[1])
    return port[1]


def process(result):
    info = []
    result['info'] = info
    result['risk_level'] = 0
    # result['risk_desc'] = 'SSH服务安全，不存在风险'
    # result['solution'] = '无'

    # // 1. 修改 ssh 的连接端口，建议改成非标准的高端端口【1024到65535】
    # // Port  22022

    os.system("netstat -tnpl4 | grep sshd > ssh.txt")
    output = open("ssh.txt", "r").readlines()
    os.remove("ssh.txt")
    print(output)
    port = getSSHPort(output)
    info.append(output)
    if port == '22':
        result['risk_desc'] = '1,ssh访问22默认端口，比较容易被攻击;\n'
        result['solution'] = '1,建议改成非标准的高端端口(1024到65535) ,\n1:修改配置文件/etc/ssh/sshd_config里端口号\n2:重启sshd服务 service sshd restart;\n'
    # else:
    #     info.append("ssh port is safety")

    # // 2. 禁止 root 用户直接登录 ssh，用普通账号 ssh 连接，然后在切换到 root 账号登录。
    # // 在/etc/ssh/sshd_config配置文件中设置以下参数
    # // PermitRootLogin  no

    output = os.popen('cat /etc/ssh/sshd_config').readlines()
    # print(output)
    bsafety = True
    for w in output:
        if str(w).upper().find('PERMITROOTLOGIN NO') >= 0:
            bsafety = False

    if(bsafety):
        result['risk_desc'] += '2,root用户可直接登录ssh\n'
        result['solution'] += '2,在/etc/ssh/sshd_config配置文件中设置以下参数 \nPermitRootLogin  no\n'

    # // 3. 限制 ssh 连接的 IP 地址，只允许用户指定的 IP 地址可以 ssh 连接服务器。
    # // 修改 /etc/hosts.allow 和 /etc/hosts.deny 这两个配置文件。
    # // vim /etc/hosts.deny     #设置禁止所有ip连接服务器的ssh。
    # // sshd:all:deny
    # // vim  /etc/hosts.allow    #设置允许指定ip连接服务器的ssh。
    # // sshd:210.xx.xx.xx:allow
    output = os.popen('cat /etc/hosts.deny').readlines()
    bsafety = True
    for w in output:
        if str(w).upper().find('SSHD:ALL:DENY') >= 0:
            bsafety = False

    if(bsafety):
        result['risk_desc'] += '3,限制 ssh 连接的 IP 地址，只允许用户指定的 IP 地址可以 ssh 连接服务器\n'
        result['solution'] += '3,修改 /etc/hosts.allow 和 /etc/hosts.deny 这两个配置文件。\nvim /etc/hosts.deny     #设置禁止所有ip连接服务器的ssh。\n# // sshd:all:deny\n    # // vim  /etc/hosts.allow    #设置允许指定ip连接服务器的ssh。\n# // sshd:210.xx.xx.xx:allow\n'

    # if len(output) == 0:
    #     result['risk_level'] = 0
    #     result['risk_desc'] = 'SSH服务没有开启'
    #     result['solution'] = '无'
    # else:
    #     result['risk_level'] = 1
    #     result['solution'] = '在命令终端中执行如下命令关闭SSH服务：\nsystemctl stop sshd.service'

    return


if __name__ == '__main__':
    info = {}
    process(info)
    print(info)
