#!/usr/bin/python3.7
# coding=utf-8

import configparser
import codecs
import os


class Config:
    def __init__(self, path):
        self.path = path
        self.cf = configparser.ConfigParser()
        self.cf.read_file(codecs.open(self.path, "r", "utf_16"))
        s = self.cf.sections()

    def get(self, field, key):
        result = str(self.cf.get(field, key))
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


def analyze(result):
    info = result['info']


if __name__ == '__main__':
    info = {}
    process(info)

    result = {'info', info}
    print(result)
