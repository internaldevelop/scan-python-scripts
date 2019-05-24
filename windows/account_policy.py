#!/usr/bin/python3.7
# coding=utf-8

import configparser
import codecs
import os

# 本脚本用于多条密码安全策略
# SCRIPT_USAGE = 1  # 账户锁定阈值（0 -- 65536），建议10次口令失败
# SCRIPT_USAGE = 2    # 账户锁定时间（0 -- 99,999分钟），建议锁定15分钟
SCRIPT_USAGE = 3    # 强制过期时间（0 -- 99,999小时），建议24小时

# refer to the page:
# https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-gpsb/2cd39c97-97cd-4859-a7b4-1229dad5f53d
# https://blog.csdn.net/yongping8204/article/details/7471627
INVALID = '-1'
MAX_LOCKOUT_THRESHOLD = 10
MIN_LOCKOUT_DURATION = 15


class Config:
    def __init__(self, path):
        self.path = path
        self.cf = configparser.ConfigParser()
        self.cf.read_file(codecs.open(self.path, "r", "utf_16"))
        s = self.cf.sections()

    def get(self, field, key):
        try:
            result = str(self.cf.get(field, key))
        except:
            return INVALID
        return result

    def set(self, field, key, value):
        self.cf.set(field, key, value)
        self.cf.write(open(self.path, 'w'))
        return True


def process(info):
    output = os.system("secedit /export /cfg Password.ini")

    cf = Config("Password.ini")

    info["Account LockoutBadCount"] = cf.get("System Access", "LockoutBadCount")
    info["Account LockoutDuration"] = cf.get("System Access", "LockoutDuration")
    info["Account ResetLockoutCount"] = cf.get("System Access", "ResetLockoutCount")
    info["Account ForceLogoffWhenHourExpire"] = cf.get("System Access", "ForceLogoffWhenHourExpire")
    info["Account NewAdministratorName"] = cf.get("System Access", "NewAdministratorName")
    info["Account Guest Active"] = cf.get("System Access", "EnableGuestAccount")

    os.remove('Password.ini')

    return


def analyze(result):
    info = result['info']
    result['risk_desc'] = ''
    result['solution'] = ''

    # 账户锁定阈值（0 -- 65536），建议10次口令失败
    if SCRIPT_USAGE == 1:
        if int(info["Account LockoutBadCount"]) > MAX_LOCKOUT_THRESHOLD:
            result['risk_level'] = 2
            result['risk_desc'] = '账户锁定阈值太大，当前设置是' + info["Account LockoutBadCount"]
            result['solution'] = '设置账户锁定阈值为3到10之间。'
        elif int(info["Account LockoutBadCount"]) <= 0:
            result['risk_level'] = 3
            result['risk_desc'] = '未设定账户锁定阈值，大大提高了账户被破解的风险'
            result['solution'] = '设置账户锁定阈值为3到10之间。'
        else:
            result['risk_level'] = 0
            result['risk_desc'] = '当前账户锁定阈值是' + info["Account LockoutBadCount"] + '，符合账户安全要求'
            result['solution'] = '无'

    # 账户锁定时间（0 -- 99,999分钟），建议锁定15分钟
    if SCRIPT_USAGE == 2:
        if int(info["Account LockoutDuration"]) <= 0:
            result['risk_level'] = 3
            result['risk_desc'] = '未设置口令试错的账户锁定时间'
            result['solution'] = '设置账户锁定时间为' + str(MIN_LOCKOUT_DURATION) + '分钟以上。'
        elif int(info["Account LockoutDuration"]) < MIN_LOCKOUT_DURATION:
            result['risk_level'] = 1
            result['risk_desc'] = '账户锁定时间过短，当前设置是' + info["Account LockoutDuration"] + '分钟。'
            result['solution'] = '设置账户锁定时间为' + str(MIN_LOCKOUT_DURATION) + '分钟以上。'
        else:
            result['risk_level'] = 0
            result['risk_desc'] = '当前账户锁定时间是' + info["Account LockoutDuration"] + '分钟，符合账户安全要求'
            result['solution'] = '无'

    # 强制过期时间（0 -- 99,999小时），建议24小时
    if SCRIPT_USAGE == 3:
        if int(info["Account ForceLogoffWhenHourExpire"]) == 0:
            result['risk_level'] = 2
            result['risk_desc'] = '未设置账户的强制过期时间'
            result['solution'] = '设置账户的强制过期时间为24小时。'
        else:
            result['risk_level'] = 0
            result['risk_desc'] = '当前账户的强制过期时间是' + info["Account ForceLogoffWhenHourExpire"] + '小时，符合账户安全要求'
            result['solution'] = '无'

    # 口令策略配置问题的解决方案增加系统策略设置路径
    if result['risk_level'] != 0:
        result['solution'] += '\n策略设置路径为：Computer Configuration\\Windows Settings\\Security Settings\\Account ' \
                              'Policies\\Password Policy '

    return


if __name__ == '__main__':
    info = {}
    process(info)

    result = {'info': info}
    analyze(result)

    print(result)
