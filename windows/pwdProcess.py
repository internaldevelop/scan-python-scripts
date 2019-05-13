#!/usr/bin/python2.7
#coding=utf-8

import ConfigParser
import codecs
import os
class Config:
    def __init__(self, path):
        
        self.path = path
        self.cf = ConfigParser.ConfigParser()
        self.cf.readfp(codecs.open(self.path, "r", "utf_16"))
        s = self.cf.sections()

    
    def get(self, field, key):
        result = ""
        try:
            result = str(self.cf.get(field, key))
        except:
            print "????",(field, key)
            result = ""
        return result
    def set(self, filed, key, value):
        try:
            self.cf.set(field, key, value)
            cf.write(open(self.path,'w'))
        except:
            return False
        return True

def read_config(config_file_path, field, key): 
    
    try:
        cf.read(config_file_path)
        result = cf.get(field, key)
    except:
        sys.exit(1)
    return result
   

def process(result):

    output = os.system("secedit /export /cfg Password.ini")

    cf = Config("Password.ini")

    result["PWD MinimumPasswordAge"]=cf.get("System Access","MinimumPasswordAge")
    result["PWD MaximumPasswordAge"]=cf.get("System Access","MaximumPasswordAge")
    result["PWD MinimumPasswordLength"]=cf.get("System Access","MinimumPasswordLength")
    result["PWD PasswordComplexity"]=cf.get("System Access","PasswordComplexity")
    result["PWD PasswordHistorySize"]=cf.get("System Access","PasswordHistorySize")
    
    result["Account LockoutBadCount"]=cf.get("System Access","LockoutBadCount")
    result["Account LockoutDuration"]=cf.get("System Access","LockoutDuration")
    result["Account ResetLockoutCount"]=cf.get("System Access","ResetLockoutCount")
    result["Account NewAdministratorName"]=cf.get("System Access","NewAdministratorName")
    result["Account Guest Active"]=cf.get("System Access","EnableGuestAccount")

    result["Audit AuditLogonEvents"]=cf.get("Event Audit","AuditLogonEvents")
    result["Audit AuditSystemEvents"]=cf.get("Event Audit","AuditSystemEvents")
    result["Audit AuditObjectAccess"]=cf.get("Event Audit","AuditObjectAccess")
    result["Audit AuditPrivilegeUse"]=cf.get("Event Audit","AuditPrivilegeUse")
    result["Audit AuditPolicyChange"]=cf.get("Event Audit","AuditPolicyChange")
    result["Audit AuditAccountManage"]=cf.get("Event Audit","AuditAccountManage")
    result["Audit AuditProcessTracking"]=cf.get("Event Audit","AuditProcessTracking")
    result["Audit AuditDSAccess"]=cf.get("Event Audit","AuditDSAccess")
    result["Audit AuditAccountLogon"]=cf.get("Event Audit","AuditAccountLogon")

    result["Log AuditLogonEvents"]=cf.get("Event Audit","AuditLogonEvents")

    os.remove('Password.ini')

if __name__ == '__main__':

    r={}
    process(r)
    print r
   