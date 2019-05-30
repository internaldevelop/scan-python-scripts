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

    result['risk_level'] = 0
    result['risk_desc'] = ''
    result['solution'] = ''

    # /etc/passwd 所有用户都可读，root用户可写
    # -rw-r--r--
    os.system("ls -l /etc/passwd > passwd.txt")
    passwd = open("passwd.txt", "r").readlines()
    if len(passwd) != 0:
        info['passwd file'] = passwd[0]
        if passwd[0][0:10] != '-rw-r--r--':
            result['risk_level'] = 2
            result['risk_desc'] += '/etc/passwd 的文件权限不符合"所有用户都可读，root用户可写"的要求。\n'
            result['solution'] += '配置命令：chmod 644 /etc/passwd 。\n'
    os.remove('passwd.txt')

    # /etc/shadow 只有root可读
    # -r--------
    os.system("ls -l /etc/shadow > shadow.txt")
    shadow = open("shadow.txt", "r").readlines()
    if len(shadow) != 0:
        info['shadow file'] = shadow[0]
        if shadow[0][0:10] != '-r--------':
            result['risk_level'] = 2
            result['risk_desc'] += '/etc/shadow 的文件权限不符合"只有root可读"的要求。\n'
            result['solution'] += '配置命令：chmod 600 /etc/shadow 。\n'
    os.remove('shadow.txt')

    # /etc/group 必须所有用户都可读，root用户可写
    # -rw-r--r--
    os.system("ls -l /etc/group > group.txt")
    group = open("group.txt", "r").readlines()
    if len(group) != 0:
        info['group file'] = group[0]
        if group[0][0:10] != '-rw-r--r--':
            result['risk_level'] = 2
            result['risk_desc'] += '/etc/group 的文件权限不符合"所有用户都可读，root用户可写"的要求。\n'
            result['solution'] += '配置命令：chmod 644 /etc/group 。\n'
    os.remove('group.txt')

    if result['risk_level'] == 0:
        result['risk_desc'] = '关键目录权限符合要求。'
        result['solution'] = '无'


if __name__ == '__main__':
    _result = {}
    process(_result)

    print(_result)
