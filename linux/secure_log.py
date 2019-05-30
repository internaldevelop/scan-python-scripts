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

    # 安全日志完备性要求
    # 系统应配置完备日志记录，记录对与系统相关的安全事件。
    os.system("grep '^authpriv' /etc/syslog.conf > syslog.txt")
    syslog = open("syslog.txt", "r").readlines()
    if len(syslog) == 0:
        info['syslog authpriv'] = '没有相应的日志配置'
        result['risk_level'] = 2
        result['risk_desc'] = '系统应配置完备日志记录，记录对与系统相关的安全事件。'
        result['solution'] = '修改配置文件vi /etc/syslog.conf，配置如下类似语句：\nauthpriv.*            /var/log/secure'
    else:
        info['syslog authpriv'] = syslog[0]
        result['risk_level'] = 0
        result['risk_desc'] = '系统已配置完备日志记录'
        result['solution'] = '无'

    os.remove('syslog.txt')


if __name__ == '__main__':
    _result = {}
    process(_result)

    print(_result)
