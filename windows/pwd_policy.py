#!/usr/bin/python3.7
# coding=utf-8

import configparser
import codecs
import os

# 本脚本用于多条密码安全策略
# SCRIPT_USAGE = 1    # 密码长度不能小于 MIN_PWD_LEN （8）
# SCRIPT_USAGE = 2    # 密码复杂度（0 -- 65536）
# SCRIPT_USAGE = 3    # 强制密码历史：新密码设定时的历史唯一性检查，检查几个历史密码 （0 -- 65536）
SCRIPT_USAGE = 4  # 密码寿命：最小密码寿命设置为1天，最大密码寿命设置为30--90天

# refer to the page:
# https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-gpsb/2cd39c97-97cd-4859-a7b4-1229dad5f53d
# https://blog.csdn.net/yongping8204/article/details/7471627
INVALID = '-1'
MIN_PWD_LEN = 8
MIN_PWD_HIS_SIZE = 5


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

    info["PWD MinimumPasswordAge"] = cf.get("System Access", "MinimumPasswordAge")
    info["PWD MaximumPasswordAge"] = cf.get("System Access", "MaximumPasswordAge")
    info["PWD MinimumPasswordLength"] = cf.get("System Access", "MinimumPasswordLength")
    info["PWD PasswordComplexity"] = cf.get("System Access", "PasswordComplexity")
    info["PWD PasswordHistorySize"] = cf.get("System Access", "PasswordHistorySize")

    info["Account LockoutBadCount"] = cf.get("System Access", "LockoutBadCount")
    info["Account LockoutDuration"] = cf.get("System Access", "LockoutDuration")
    info["Account ResetLockoutCount"] = cf.get("System Access", "ResetLockoutCount")
    info["Account NewAdministratorName"] = cf.get("System Access", "NewAdministratorName")
    info["Account Guest Active"] = cf.get("System Access", "EnableGuestAccount")

    info["Audit AuditLogonEvents"] = cf.get("Event Audit", "AuditLogonEvents")
    info["Audit AuditSystemEvents"] = cf.get("Event Audit", "AuditSystemEvents")
    info["Audit AuditObjectAccess"] = cf.get("Event Audit", "AuditObjectAccess")
    info["Audit AuditPrivilegeUse"] = cf.get("Event Audit", "AuditPrivilegeUse")
    info["Audit AuditPolicyChange"] = cf.get("Event Audit", "AuditPolicyChange")
    info["Audit AuditAccountManage"] = cf.get("Event Audit", "AuditAccountManage")
    info["Audit AuditProcessTracking"] = cf.get("Event Audit", "AuditProcessTracking")
    info["Audit AuditDSAccess"] = cf.get("Event Audit", "AuditDSAccess")
    info["Audit AuditAccountLogon"] = cf.get("Event Audit", "AuditAccountLogon")

    info["Log AuditLogonEvents"] = cf.get("Event Audit", "AuditLogonEvents")

    os.remove('Password.ini')

    return


def analyze(result):
    info = result['info']
    result['risk_desc'] = ''
    result['solution'] = ''

    # 密码长度不能小于 MIN_PWD_LEN （8）
    if SCRIPT_USAGE == 1:
        if int(info["PWD MinimumPasswordLength"]) < MIN_PWD_LEN:
            result['risk_level'] = 3
            result['risk_desc'] = '允许设置的密码长度太短'
            result['solution'] = '设置密码长度最少为' + str(MIN_PWD_LEN) + '位。'
        else:
            result['risk_level'] = 0
            result['risk_desc'] = '密码长度符合要求'
            result['solution'] = '无'

    # 密码复杂度（0 -- 65536）
    if SCRIPT_USAGE == 2:
        if int(info["PWD PasswordComplexity"]) < 1:
            result['risk_level'] = 3
            result['risk_desc'] = '没有限制密码的复杂度'
            result['solution'] = '密码不能含用户名，需包含大写字母、小写字母、数字及特殊字符。'
        else:
            result['risk_level'] = 0
            result['risk_desc'] = '密码复杂度符合要求'
            result['solution'] = '无'

    # 强制密码历史：新密码设定时的历史唯一性检查，检查几个历史密码 （0 -- 65536）
    if SCRIPT_USAGE == 3:
        if int(info["PWD PasswordHistorySize"]) < MIN_PWD_HIS_SIZE:
            result['risk_level'] = 3
            result['risk_desc'] = '强制密码历史不符合要求，当前系统设置为' + info["PWD PasswordHistorySize"] + '个记住密码'
            result['solution'] = '设置强制密码历史数最少为' + str(MIN_PWD_HIS_SIZE) + '个记住密码。'
        else:
            result['risk_level'] = 0
            result['risk_desc'] = '强制密码历史符合要求'
            result['solution'] = '无'

    # 密码寿命：最小密码寿命设置为1天，最大密码寿命设置为30--90天
    if SCRIPT_USAGE == 4:
        if 30 <= int(info["PWD MaximumPasswordAge"]) <= 90:
            if int(info["PWD MinimumPasswordAge"]) == 1:
                result['risk_level'] = 0
                result['risk_desc'] = '口令寿命符合要求'
                result['solution'] = '无'
            else:
                result['risk_level'] = 1
                result['risk_desc'] = '最小密码寿命设置不合理，当前设置为' + info["PWD MinimumPasswordAge"] + '天'
                result['solution'] = '设置最小密码寿命为1天。'
        else:
            result['risk_level'] = 2
            result['risk_desc'] = '最大密码寿命不符合要求，当前设置为' + info["PWD MaximumPasswordAge"] + '天'
            result['solution'] = '设置最大密码寿命为30到90天。'

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
