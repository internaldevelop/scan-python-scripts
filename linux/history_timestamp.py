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

    # 设置history时间戳，便于审计。
    # 系统应配置完备日志记录，记录对与系统相关的安全事件。
    os.system("grep HISTTIMEFORMAT /etc/profile > history.txt")
    history = open("history.txt", "r").readlines()
    if len(history) == 0:
        info['History timestamp'] = '没有配置 history 时间戳。'
        result['risk_level'] = 1
        result['risk_desc'] = '系统应配置 history 时间戳，便于审计。'
        result['solution'] = '在/etc/profile 文件中增加如下行：\nexport HISTTIMEFORMAT="%F %T `whoami` "'
    else:
        info['History timestamp'] = history[0]
        result['risk_level'] = 0
        result['risk_desc'] = '系统已配置 history 时间戳。'
        result['solution'] = '无'

    os.remove('history.txt')


if __name__ == '__main__':
    _result = {}
    process(_result)

    print(_result)
