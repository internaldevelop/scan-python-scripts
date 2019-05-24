#!/usr/bin/python3.7
# coding=utf-8
import os
import winreg

# SCRIPT_USAGE = 1  # 抵御 ICMP 攻击
# SCRIPT_USAGE = 2  # 抵御 SYN 攻击
# SCRIPT_USAGE = 3  # 抵御 SNMP 攻击
SCRIPT_USAGE = 4  # 其它网络保护


def getRegValue(key, value_name):
    try:
        value, type = winreg.QueryValueEx(key, value_name)
    except WindowsError:
        value = -1

    return value


def process_and_anylyze(result):
    info = {}
    result['info'] = info
    result['risk_level'] = 0
    result['risk_desc'] = '未发现网络配置缺陷。'
    result['solution'] = '无'

    if SCRIPT_USAGE == 1:
        # ===================================================================
        # 打开注册表 HKLM\System\CurrentControlSet\Services\AFD\Parameters
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'System\CurrentControlSet\Services\AFD\Parameters')

        # EnableICMPRedirect：ICMP 重定向数据包的处理
        # 有效值：0（禁用），1（启用）。建议值：0
        value = getRegValue(key, 'EnableICMPRedirect')
        info['EnableICMPRedirect'] = value
        if value != 0:
            result['risk_level'] = 1
            result['risk_desc'] = '没有禁用 ICMP 重定向数据包，易受到ICMP攻击。'
            result[
                'solution'] = '设置注册表项 HKLM\System\CurrentControlSet\Services\AFD\Parameters下的键值：EnableICMPRedirect = 0。'
        return

    # ===================================================================
    # 打开注册表 HKLM\System\CurrentControlSet\Services\Tcpip\Parameters
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'System\CurrentControlSet\Services\Tcpip\Parameters')

    if SCRIPT_USAGE == 2:
        # SynAttackProtect 机制是通过关闭某些socket选项，增加额外的连接指示和减少超时时间，使系统能处理更多的SYN连接，以达到防范SYN攻击的目的
        # 缺省没有这个键值，系统不受 SynAttackProtect 保护。建议值：2
        # 有效值：0，系统不受 SynAttackProtect 保护
        # 有效值：1，系统通过减少重传次数和延迟未连接时路由缓冲项（route cache entry）防范SYN攻击
        # 有效值：2，系统不仅使用backlog队列，还使用附加的半连接指示，以此来处理更多的SYN连接，使用此键值时，tcp/ip的TCPInitialRTT、window size和可滑动窗囗将被禁止
        value = getRegValue(key, 'SynAttackProtect')
        info['SynAttackProtect'] = value
        if value == 1:
            result['risk_level'] = 1
            result['risk_desc'] = '系统通过减少重传次数和延迟未连接时路由缓冲项（route cache entry）防范SYN攻击，为进一步降低SYN攻击风险，可以禁止TCP/IP滑动窗口。'
            result['solution'] = '设置注册表项 HKLM\System\CurrentControlSet\Services\Tcpip\Parameters下的键值：SynAttackProtect ' \
                                 '= 2，系统不仅使用backlog队列，还使用附加的半连接指示，以此来处理更多的SYN连接，使用此键值时，tcp/ip的TCPInitialRTT、window ' \
                                 'size和可滑动窗囗将被禁止 '
        elif value <= 0:
            result['risk_level'] = 2
            result['risk_desc'] = '系统不受 SynAttackProtect 保护，无法有效防范SYN攻击。'
            result['solution'] = '设置注册表项 HKLM\System\CurrentControlSet\Services\Tcpip\Parameters下的键值：SynAttackProtect ' \
                                 '= 2，系统不仅使用backlog队列，还使用附加的半连接指示，以此来处理更多的SYN连接，使用此键值时，tcp/ip的TCPInitialRTT、window ' \
                                 'size和可滑动窗囗将被禁止 '
        return

    if SCRIPT_USAGE == 3:
        # EnableDeadGWDetect 禁止攻击者强制切换到备用网关
        # 有效值：0（禁用），1（启用）
        # 建议的数值数据： 0
        value = getRegValue(key, 'EnableDeadGWDetect')
        info['EnableDeadGWDetect'] = value
        if value != 0:
            result['risk_level'] = 2
            result['risk_desc'] = '系统没有禁止攻击者强制切换到备用网关，无法有效抵御 SNMP 攻击。'
            result['solution'] = '设置注册表项 HKLM\System\CurrentControlSet\Services\Tcpip\Parameters' \
                                 '下的键值：EnableDeadGWDetect = 0，系统不仅使用backlog队列，还使用附加的半连接指示，以此来处理更多的SYN连接，使用此键值时，tcp/ip' \
                                 '的TCPInitialRTT、window size和可滑动窗囗将被禁止 '
        return

    if SCRIPT_USAGE == 4:
        # DisableIPSourceRouting
        # 禁用 IP 源路由，后者允许发送者确认数据报在网络中应采用的路由。
        # 有效值：0（转发所有数据包），1（不转发源路由数据包），2（丢弃所有传入的源路由数据包）。
        # 建议的数值数据： 1
        value = getRegValue(key, 'DisableIPSourceRouting')
        info['DisableIPSourceRouting'] = value
        if value >= 2:
            result['risk_level'] = 1
            result['risk_desc'] = '系统丢弃所有传入的源路由数据包。'
            result['solution'] = '设置注册表项 HKLM\System\CurrentControlSet\Services\Tcpip\Parameters' \
                                 '下的键值：DisableIPSourceRouting = 1，禁用 IP 源路由，不允许发送者确认数据报在网络中应采用的路由。 '
        elif value <= 0:
            result['risk_level'] = 2
            result['risk_desc'] = '系统转发所有数据包，攻击者可能规避 NAT 屏蔽，以便使用 IP 源路由来确定网络拓扑。'
            result['solution'] = '设置注册表项 HKLM\System\CurrentControlSet\Services\Tcpip\Parameters' \
                                 '下的键值：DisableIPSourceRouting = 1，禁用 IP 源路由，不允许发送者确认数据报在网络中应采用的路由。 '

    return


if __name__ == '__main__':
    _result = {}
    process_and_anylyze(_result)

    print(_result)
