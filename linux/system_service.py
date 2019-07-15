import os
import platform
import json
import re


def get_os_info():
    os_info = platform.uname()._asdict()
    return os_info


def is_service_running(info_list, service):
    if len(info_list) > 0:
        for info in info_list:
            if info.find(service) >= 0:
                return True
    return False


def process(result):
    info = {}
    result['info'] = info

    os_info = get_os_info()

    result['risk_level'] = 0
    result['risk_desc'] = ''
    result['solution'] = ''

    # 获取所有系统服务
    os.system("systemctl list-units > services.txt")
    services = open("services.txt", "r").readlines()
    info['Running Services'] = services

    # Linux/Unix系统服务中，部分服务存在较高安全风险，应当禁用，包括：
    # “lpd”，此服务为行式打印机后台程序，用于假脱机打印工作的UNIX后台程序，此服务通常情况下不用，建议禁用；
    # “telnet”，此服务采用明文传输数据，登陆信息容易被窃取，建议用ssh代替；
    # “routed”，此服务为路由守候进程，使用动态RIP路由选择协议，建议禁用；
    # “sendmail”，此服务为邮件服务守护进程，非邮件服务器应将其关闭；
    # “Bluetooth”，此服务为蓝牙服务，如果不需要蓝牙服务时应关闭；
    # “identd”，此服务为AUTH服务，在提供用户信息方面与finger类似，一般情况下该服务不是必须的，建议关闭；
    # “xfs”，此服务为Linux中X Window的字体服务，关于该服务历史上出现过信息泄露和拒绝服务等漏洞，应以减少系统风险；
    # R服务（“rlogin”、“rwho”、“rsh”、“rexec”），R服务设计上存在严重的安全缺陷，仅适用于封闭环境中信任主机之间便捷访问，其他场合下均必须禁用；
    # 基于inetd/xinetd的服务（daytime、chargen、echo等），此类服务建议禁用。
    check_list = ['lpd', 'telnet', 'routed', 'sendmail', 'Bluetooth', 'identd', 'xfs',
                  'rlogin', 'rwho', 'rsh', 'rexec', 'inetd', 'xinetd']
    for service in check_list:
        if is_service_running(services, service):
            result['risk_level'] = 2
            result['risk_desc'] += '系统启动了 {} 服务，该服务有安全风险。\n'.format(service)
            result['solution'] += '关闭 {} 服务，且将其设置成开机不自动启动。\n'.format(service)

    if result['risk_level'] == 0:
        result['risk_desc'] = '未发现有安全风险的系统服务。'
        result['solution'] = '无'

    os.remove('services.txt')


if __name__ == '__main__':
    _result = {}
    process(_result)

    print(_result)
