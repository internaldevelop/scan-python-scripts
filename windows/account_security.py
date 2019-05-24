#!/usr/bin/python3.7
# coding=utf-8
import os


def getAdmin(line):
    return [i.strip() for i in line[6:-2]]


def getUser(line):
    result = []
    for i in line[4:-2]:
        result += i.split()
    return result


def getValue(lines, key):
    r = ''
    for i in lines:
        v = i.split()
        if len(v) > 2:
            if key == v[0]:
                r = v[-1]
    return r


def process(info):
    # 检查管理员权限账户
    output = os.system("net localgroup administrators >Account_admin.log")
    info['Account Admin'] = getAdmin(open("Account_admin.log", 'r').readlines())

    # 检查所有账户
    output = os.system("net user >Account_user.log")
    info['Account Users'] = getUser(open("Account_user.log", 'r').readlines())
    for i in info['Account Users']:
        output = os.system("net user %s >>Account_Info.log" % i)
    line = open("Account_Info.log", 'r').readlines()
    num = len(info['Account Users'])

    # 检查账户启用情况
    info['Account Active'] = [[info['Account Users'][i], line[5 + i * 26].split('  ')[-1].strip()] for i in
                              range(num)]

    # 检查账户是否需要密码
    info['Account Password Required'] = [[info['Account Users'][i], line[11 + i * 26].split('  ')[-1].strip()] for i
                                         in range(num)]

    # 检查上一次设置密码时间
    info['Account Password Last set'] = [[info['Account Users'][i], line[8 + i * 26].split('  ')[-1].strip()] for i
                                         in range(num)]

    # 检查是否禁止匿名用户空链接
    r = os.system("reg query HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Lsa\ >reg.log")
    info["Account Restrict Anonymous"] = getValue(open("reg.log", 'r').readlines(), "restrictanonymous")

    # 检查是否开启自动登录
    r = os.system('reg query HKEY_LOCAL_MACHINE\Software\Microsoft\Windows" "NT\CurrentVersion\Winlogon\ >reg.log')
    info["Account AutoAdminLogon"] = getValue(open("reg.log", 'r').readlines(), "AutoAdminLogon")

    os.remove('Account_admin.log')
    os.remove('Account_user.log')
    os.remove('Account_Info.log')
    os.remove("reg.log")

    return


def analyze(result):
    info = result['info']

    result['risk_level'] = 0
    result['risk_desc'] = ''
    for index in range(len(info['Account Users'])):
        account = info['Account Users'][index]
        acc_active = info['Account Active'][index]
        acc_require_pwd = info['Account Password Required'][index]

        # 检查两个对象的账户名是否一致
        if acc_active[0] != acc_require_pwd[0]:
            continue

        # 检查是否存在：激活账户不需要口令的情况
        if acc_active[1] == 'Yes' and acc_require_pwd[1] != 'Yes':
            result['risk_level'] = 3
            result['risk_desc'] += '账户{acc_active[0]}是激活账户，但登陆不需要口令，对系统访问构成了较大风险。\n'
            result['solution'] = '检查系统所有账户的激活状态，以及是否需要口令，确保所有激活账户强制口令校验。'

    if result['risk_level'] == 0:
        result['risk_desc'] = '系统所有账户激活和口令配置正常'
        result['solution'] = '无'

    return


if __name__ == '__main__':
    _info = {}
    process(_info)

    _result = {'info': _info}
    analyze(_result)

    print(_result)
