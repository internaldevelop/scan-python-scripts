#!/usr/bin/python3.7
# coding=utf-8
import os
import winreg


def getRegValue(key, value_name):
    try:
        value, type = winreg.QueryValueEx(key, value_name)
    except WindowsError:
        value = -1
        type = -1

    return value, type


def process(result):
    info = {}
    result['info'] = info

    # 打开注册表 HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced\Folder\Hidden\SHOWALL
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced'
                                                    r'\Folder\Hidden\SHOWALL')

    # 读取系统隐藏文件的可读性
    value, type = getRegValue(key, 'CheckedValue')
    # 键值类型4：REG_DWORD
    if type != 4 or value != 1:
        info['Hide File Defect'] = 1
        result['risk_level'] = 3
        result['risk_desc'] = '木马修改了注册表，以保护自己，需修复注册表。'
        result['solution'] = '在注册表 HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced' \
                             '\Folder\Hidden\SHOWALL下，将CheckedValue删除，再新建一个DWORD值命名为CheckedValue，数值取1即可。 '
    else:
        info['Hide File Defect'] = 0
        result['risk_level'] = 0
        result['risk_desc'] = '未发现隐藏文件漏洞。'
        result['solution'] = '无'

    return


if __name__ == '__main__':
    _result = {}
    process(_result)

    print(_result)
