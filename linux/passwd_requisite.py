import os
import platform
import json
import re


def get_os_info():
    os_info = platform.uname()._asdict()
    return os_info


def process(result):
    info = {}
    result['info'] = info

    os_info = get_os_info()

    # 获取密码要求的配置
    os.system("grep '^password\t*requisite' /etc/pam.d/common-password > passwd_req.txt")
    passwd_req = open("passwd_req.txt", "r").readlines()

    # password requisite pam_deny.so minlen=6
    # 参数说明如下：
    # 1、retry=N，确定用户创建密码时允许重试的次数；
    # 2、minlen=N，确定密码最小长度要求，事实上，在默认配置下，此参数代表密码最小长度为N-1；
    # 3、dcredit=N，当N小于0时，代表新密码中数字字符数量不得少于（-N）个。例如，dcredit=-2代表密码中要至少包含两个数字字符；
    # 4、ucredit=N，当N小于0时，代表则新密码中大写字符数量不得少于（-N）个；
    # 5、lcredit=N，当N小于0时，代表则新密码中小写字符数量不得少于（-N）个；
    # 6、ocredit=N，当N小于0时，代表则新密码中特殊字符数量不得少于（-N）个；
    if len(passwd_req) == 0:
        # 如果读取不到 password requisite 参数，按没有密码要求处理
        info['Password requisite'] = "没有找到口令要求的配置。"
        result['risk_level'] = 2
        result['risk_desc'] = '系统没有对用户口令做任何限制要求，用户口令可能过于简单，对系统造成威胁。'
        result['solution'] = '修改/etc/pam.d/common-password文件，设置password requisite minlen = 12。'
    else:
        # passwd_req = 'password    requisite     minlen = 8'
        passwd_req = passwd_req[0]
        info['Password requisite'] = passwd_req
        pos = passwd_req.find('minlen')
        if pos < 0:
            result['risk_level'] = 1
            result['risk_desc'] = '未设置口令最小长度，系统安全要求最少12位。'
            result['solution'] = 'vi /etc/pam.d/common-password，找到password模块接口的配置部分，设置password requisite minlen = 12。'
        else:
            min_len = passwd_req[pos:].strip().replace(' ', '')
            min_len = int(min_len[7:])
            if min_len < 12:
                result['risk_level'] = 1
                result['risk_desc'] = '当前口令最小长度设置为{}位，系统安全要求最少12位。'.format(min_len)
                result['solution'] = 'vi /etc/pam.d/common-password，找到password模块接口的配置部分，设置password requisite minlen = ' \
                                     '12。 '
            else:
                result['risk_level'] = 0
                result['risk_desc'] = '用户口令设置符合要求。'
                result['solution'] = '无'

    os.remove("passwd_req.txt")


if __name__ == '__main__':
    _result = {}
    process(_result)

    print(_result)
