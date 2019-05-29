#!/usr/bin/python3.7
# coding=utf-8

import configparser
import codecs
import os

# 本脚本用于多条审计策略
# SCRIPT_USAGE = 1    # 登录日志审计策略
# SCRIPT_USAGE = 2    # 系统事件审计策略
# SCRIPT_USAGE = 3    # 对象访问事件审计策略
# SCRIPT_USAGE = 4  # 特权使用事件审计策略
# SCRIPT_USAGE = 5    # 策略更改事件审计策略
# SCRIPT_USAGE = 6    # 账户管理事件审计策略
# SCRIPT_USAGE = 7    # 过程追踪事件审计策略
# SCRIPT_USAGE = 8    # 目录服务事件审计策略
SCRIPT_USAGE = 9    # 账户登录事件审计策略

INVALID = '-1'


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

    info["Audit AuditLogonEvents"] = cf.get("Event Audit", "AuditLogonEvents")
    info["Audit AuditSystemEvents"] = cf.get("Event Audit", "AuditSystemEvents")
    info["Audit AuditObjectAccess"] = cf.get("Event Audit", "AuditObjectAccess")
    info["Audit AuditPrivilegeUse"] = cf.get("Event Audit", "AuditPrivilegeUse")
    info["Audit AuditPolicyChange"] = cf.get("Event Audit", "AuditPolicyChange")
    info["Audit AuditAccountManage"] = cf.get("Event Audit", "AuditAccountManage")
    info["Audit AuditProcessTracking"] = cf.get("Event Audit", "AuditProcessTracking")
    info["Audit AuditDSAccess"] = cf.get("Event Audit", "AuditDSAccess")
    info["Audit AuditAccountLogon"] = cf.get("Event Audit", "AuditAccountLogon")

    os.remove('Password.ini')

    return


def check_audit(audit_key, audit_type):
    info = result['info']
    value = info['Audit ' + audit_key]
    if int(value) == 3:
        result['risk_level'] = 0
        result['risk_desc'] = f'{audit_type}审计策略配置正确'
        result['solution'] = '无'
    elif int(value) == 0:
        result['risk_level'] = 2
        result['risk_desc'] = f'系统没有配置{audit_type}审计策略，存在较严重的审计缺陷'
        result['solution'] = f'设置{audit_key}的审计策略为：成功事件+失败事件。'
    elif int(value) == 1:
        result['risk_level'] = 1
        result['risk_desc'] = f'系统只配置了{audit_type}的成功事件审计'
        result['solution'] = f'设置{audit_key}的审计策略为：成功事件+失败事件。'
    elif int(value) == 2:
        result['risk_level'] = 1
        result['risk_desc'] = f'系统只配置了{audit_type}的失败事件审计'
        result['solution'] = f'设置{audit_key}的审计策略为：成功事件+失败事件。'

    if result['risk_level'] != 0:
        result['solution'] += '审计安全设置的位置是：Computer Configuration\Windows Settings\Security Settings\Local ' \
                              'Policies\Audit Policy '


# 检查审计策略的设定值：
# 0：不审计
# 1：审计成功事件
# 2：审计失败事件
# 3：审计成功、失败事件
def analyze(result):
    info = result['info']
    result['risk_level'] = 0
    result['risk_desc'] = '审计策略配置正确'
    result['solution'] = '无'

    # 登录日志审计策略
    if SCRIPT_USAGE == 1:
        check_audit('AuditLogonEvents', '登录')

    # 系统事件审计策略
    if SCRIPT_USAGE == 2:
        check_audit('AuditSystemEvents', '系统')

    # 对象访问事件审计策略
    if SCRIPT_USAGE == 3:
        check_audit('AuditObjectAccess', '对象访问')

    # 特权使用事件审计策略
    if SCRIPT_USAGE == 4:
        check_audit('AuditPrivilegeUse', '特权使用')

    # 策略更改事件审计策略
    if SCRIPT_USAGE == 5:
        check_audit('AuditPolicyChange', '策略更改')

    # 账户管理事件审计策略
    if SCRIPT_USAGE == 6:
        check_audit('AuditAccountManage', '账户管理')

    # 过程追踪事件审计策略
    if SCRIPT_USAGE == 7:
        check_audit('AuditProcessTracking', '过程追踪')

    # 目录服务事件审计策略
    if SCRIPT_USAGE == 8:
        check_audit('AuditDSAccess', '目录服务')

    # 账户登录事件审计策略
    if SCRIPT_USAGE == 9:
        check_audit('AuditAccountLogon', '账户登录')


    return


if __name__ == '__main__':
    info = {}
    process(info)

    result = {'info': info}
    analyze(result)

    print(result)
