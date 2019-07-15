import os
import platform
import json
import re


def get_os_info():
    os_info = platform.uname()._asdict()
    return os_info


def check_config(cfg_list, cfg, value):
    if len(cfg_list) > 0:
        for info in cfg_list:
            if info.find(cfg) == 0 and info.find(value) > len(cfg):
                return True
    return False


def get_line(info_list, key):
    if len(info_list) > 0:
        for info in info_list:
            if info.find(key) >= 0:
                return info
    return ''


def process(result):
    info = {}
    result['info'] = info

    os_info = get_os_info()

    result['risk_level'] = 0
    result['risk_desc'] = ''
    result['solution'] = ''

    # SSH登录配置
    # 系统应配置使用SSH等加密协议进行远程登录维护，并安全配置SSHD的设置。不使用TELENT进行远程登录维护。

    # 检查 ssh 服务
    os.system("ps -elf | grep sshd > ps.txt")
    ps_result = open("ps.txt", "r").readlines()
    line_info = get_line(ps_result, '/usr/sbin/sshd')
    if len(line_info) == 0:
        info['SSH Service'] = '没有启动 SSH 服务。'
        result['risk_level'] = 2
        result['risk_desc'] += '没有启动SSH服务。\n'
        result['solution'] += '命令：systemctl start sshd 启动服务\n'
    else:
        info['SSH Service'] = line_info

    # 检查 telnet 服务
    os.system("ps -elf | grep xinetd > ps.txt")
    ps_result = open("ps.txt", "r").readlines()
    line_info = get_line(ps_result, '/etc/rc.d/init.d/xinetd')
    if len(line_info) > 0:
        info['Telnet Service'] = line_info
        result['risk_level'] = 2
        result['risk_desc'] += '系统启动了 Telnet 服务，采用这种远程维护是不安全的。\n'
        result['solution'] += '关闭 Telnet 服务，且将其设置成开机不自动启动。\n'
    else:
        info['Telnet Service'] = '没有启动 Telnet 服务。'

    os.remove('ps.txt')

    # 读取 SSH 配置
    os.system("cat /etc/ssh/sshd_config > sshd_config.txt")
    sshd_config = open("sshd_config.txt", "r").readlines()
    info['SSH Config'] = sshd_config

    # 窗口图形传输使用ssh加密
    if not check_config(sshd_config, 'X11Forwarding', 'yes'):
        result['risk_level'] = 2
        result['risk_desc'] += '未允许窗口图形传输使用 SSH 加密。\n'
        result['solution'] += 'sshd_config 增加配置：X11Forwarding yes。\n'

    # 完全禁止SSHD使用.rhosts文件
    if not check_config(sshd_config, 'IgnoreRhosts', 'yes'):
        result['risk_level'] = 2
        result['risk_desc'] += '未禁止SSHD使用.rhosts文件。\n'
        result['solution'] += 'sshd_config 增加配置：IgnoreRhosts yes。\n'

    # 不设置使用基于rhosts的安全验证
    if not check_config(sshd_config, 'RhostsAuthentication', 'no'):
        result['risk_level'] = 2
        result['risk_desc'] += '未禁止基于rhosts的安全验证。\n'
        result['solution'] += 'sshd_config 增加配置：RhostsAuthentication no。\n'

    # 不设置使用RSA算法的基于rhosts的安全验证
    if not check_config(sshd_config, 'RhostsRSAAuthentication', 'no'):
        result['risk_level'] = 2
        result['risk_desc'] += '未禁止使用RSA算法的基于rhosts的安全验证。\n'
        result['solution'] += 'sshd_config 增加配置：RhostsRSAAuthentication no。\n'

    # 不允许基于主机白名单方式认证
    if not check_config(sshd_config, 'HostbasedAuthentication', 'no'):
        result['risk_level'] = 2
        result['risk_desc'] += '未禁止基于主机白名单方式认证。\n'
        result['solution'] += 'sshd_config 增加配置：HostbasedAuthentication no。\n'

    # 不允许root登录
    if not check_config(sshd_config, 'PermitRootLogin', 'no'):
        result['risk_level'] = 2
        result['risk_desc'] += '未禁止root登录。\n'
        result['solution'] += 'sshd_config 增加配置：PermitRootLogin no。\n'

    # 不允许空密码
    if not check_config(sshd_config, 'PermitEmptyPasswords', 'no'):
        result['risk_level'] = 2
        result['risk_desc'] += '未禁止空密码。\n'
        result['solution'] += 'sshd_config 增加配置：PermitEmptyPasswords no。\n'

    # 设置ssh登录时显示的banner
    if not check_config(sshd_config, 'Banner', '/etc/motd'):
        result['risk_level'] = 2
        result['risk_desc'] += '未设置ssh登录时显示的banner。\n'
        result['solution'] += 'sshd_config 增加配置：Banner /etc/motd。\n'

    os.remove('sshd_config.txt')


if __name__ == '__main__':
    _result = {}
    process(_result)

    print(_result)
