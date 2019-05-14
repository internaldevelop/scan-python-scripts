#!/usr/bin/python3.7
# coding=utf-8
import os
# import sys


def getValue(t):
    try:
        return t[t.index(':') + 1:].strip()
    except ValueError:
        return ''


def getSCValue(line):
    try:
        return line[3].split(":")[1].strip()
    except ValueError:
        return 'Not Installed'


def process(info):
    output = os.system("systeminfo >system_info.log")
    line_array = open("system_info.log", "r").readlines()

    info["OS Host Name"] = getValue(line_array[1])
    info["OS Name"] = getValue(line_array[2])
    info["OS Version"] = getValue(line_array[3])
    info["OS Manufacturer"] = getValue(line_array[4])
    info["OS Configuration"] = getValue(line_array[5])
    info["OS Build Type"] = getValue(line_array[6])
    info["OS Registered Owner"] = getValue(line_array[7])
    info["OS Registered Organization"] = getValue(line_array[8])
    info["OS Product ID"] = getValue(line_array[9])
    info["OS Original Install Date"] = getValue(line_array[10])
    info["System Boot Time"] = getValue(line_array[11])
    info["System Manufacturer"] = getValue(line_array[12])
    info["System Model"] = getValue(line_array[13])
    info["System Type"] = getValue(line_array[14])

    line_num = 16
    for i in range(line_num, len(line_array)):
        if line_array[i][0] != ' ':
            line_num = i
            break
    info["System Processor(s)"] = [i.strip() for i in line_array[16:line_num]]

    info["System BIOS Version"] = getValue(line_array[line_num])
    line_num = line_num + 1

    info["OS Windows Directory"] = getValue(line_array[line_num])
    line_num = line_num + 1

    info["System Directory"] = getValue(line_array[line_num])
    line_num = line_num + 1

    info["System Boot Device"] = getValue(line_array[line_num])
    line_num = line_num + 1

    info["OS Locale"] = getValue(line_array[line_num])
    line_num = line_num + 1

    info["OS Input Locale"] = getValue(line_array[line_num])
    line_num = line_num + 1

    info["OS Time Zone"] = getValue(line_array[line_num])
    line_num = line_num + 1

    info["System Total Physical Memory"] = getValue(line_array[line_num])
    line_num = line_num + 1

    info["System Available Physical Memory"] = getValue(line_array[line_num])
    line_num = line_num + 1

    info["OS Virtual Memory: Max Size"] = getValue(line_array[line_num])
    line_num = line_num + 1

    info["OS Virtual Memory: Available"] = getValue(line_array[line_num])
    line_num = line_num + 1

    info["OS Virtual Memory: In Use"] = getValue(line_array[line_num])
    line_num = line_num + 1

    info["OS Page File Location(s)"] = getValue(line_array[line_num])
    line_num = line_num + 1

    info["OS Domain"] = getValue(line_array[line_num])
    line_num = line_num + 1

    info["OS Logon Server"] = getValue(line_array[line_num])

    line_num = line_num + 2

    end_num = line_num
    for i in range(line_num, len(line_array)):
        if line_array[i][0] != ' ':
            end_num = i
            break
    info["OS Hotfix(s)"] = [i.strip() for i in line_array[line_num:end_num]]

    output = os.system("sc query wscsvc >system_Alerter.log")
    info['System Alerter'] = getSCValue(open("system_Alerter.log", 'r').readlines())

    output = os.system("sc query wuauserv >system_autoupdate.log")
    info['System Autoupdate'] = getSCValue(open("system_autoupdate.log", 'r').readlines())

    os.remove('system_info.log')
    os.remove('system_Alerter.log')
    os.remove('system_autoupdate.log')

    return


def analyze(result):
    info = result['info']
    fix_num = len(info['OS Hotfix(s)'])
    if fix_num == 0:
        result['risk_level'] = 3
        result['risk_desc'] = '未安装系统补丁，有较严重的安全隐患'
        result['solution'] = '配置Windows Update，连接互联网，更新系统修补程序。'
    elif 0 < fix_num < 10:
        result['risk_level'] = 1
        result['risk_desc'] = '系统补丁过少，存在安全风险'
        result['solution'] = '配置Windows Update，连接互联网，更新系统修补程序。'
    else:
        result['risk_level'] = 0
        result['risk_desc'] = '系统信息正常'
        result['solution'] = '无'
    return


if __name__ == '__main__':
    info = {}
    process(info)

    result = {'info': info}
    analyze(result)

    print(result)
