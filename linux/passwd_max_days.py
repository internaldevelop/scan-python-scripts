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
    os.system("grep '^PASS_MAX_DAYS' /etc/login.defs > pass_maxd.txt")
    pass_max_days_list = open("pass_maxd.txt", "r").readlines()

    # cat /etc/login.defs文件中指定配置项，其中：
    # 要求操作系统的账户口令的最长生存期不长于90天
    # PASS_MAX_DAYS配置项决定密码最长使用期限；
    # PASS_MIN_DAYS配置项决定密码最短使用期限；
    # PASS_WARN_AGE配置项决定密码到期提醒时间。
    # vi /etc/login.defs文件，修改PASS_MAX_DAYS值为小于等于90
    if len(pass_max_days_list) == 0:
        # 如果读取不到 PASS_MAX_DAYS 配置，按没有该配置处理
        info['PASS_MAX_DAYS'] = "没有设置口令的最长使用期限。"
        result['risk_level'] = 2
        result['risk_desc'] = '没有设置口令的最长使用期限。'
        result['solution'] = '配置方法：vi /etc/login.defs文件，修改PASS_MAX_DAYS值为小于等于90。'
    else:
        # PASS_MAX_DAYS	99999
        pass_max_days = pass_max_days_list[0]
        info['PASS_MAX_DAYS'] = pass_max_days
        pass_max_days = re.sub(' +', ' ', pass_max_days)
        pass_max_days = int(pass_max_days.split()[1])
        if pass_max_days > 90:
            result['risk_level'] = 1
            result['risk_desc'] = '账户口令的最长生存期的当前设置为{}天,违背了不长于90天的原则。'.format(pass_max_days)
            result['solution'] = '配置方法：vi /etc/login.defs文件，修改PASS_MAX_DAYS值为小于等于90。'
        else:
            result['risk_level'] = 0
            result['risk_desc'] = '账户口令的最长生存期的当前设置为{}天，符合不长于90天的要求。'.format(pass_max_days)
            result['solution'] = '无'

    os.remove("pass_maxd.txt")


if __name__ == '__main__':
    _result = {}
    process(_result)

    print(_result)
