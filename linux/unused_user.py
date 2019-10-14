import os
import platform
import json

# for test github user login
# for test github user login 2nd

def get_os_info():
    os_info = platform.uname()._asdict()
    return os_info


def process(result):
    info = {}
    result['info'] = info

    os_info = get_os_info()
    # os_json = json.dumps(os_info)
    # print(os_info)
    # print(os_json)

    # 获取所有用户
    os.system("cat /etc/passwd > passwd.txt")
    all_users = open("passwd.txt", "r").readlines()

    # 获取所有有效用户 (每行结尾不是 nologin)
    os.system("grep -v nologin$ /etc/passwd > passwd.txt")
    active_users = open("passwd.txt", "r").readlines()

    all_users_count = len(all_users)
    active_users_count = len(active_users)
    info['Active Users'] = active_users

    # 活跃用户大于5时，需检查确认是否有多余账户
    if active_users_count > 5:
        result['risk_level'] = 1
        result['risk_desc'] = '系统账户过多，共计{}个账户，其中{}个活跃账户。'.format(all_users_count, active_users_count)
        result['solution'] = '请联系系统管理员，使用超级用户登录系统，锁定与设备或系统运行、维护等工作无关的帐号\npasswd -l <username>'
    else:
        result['risk_level'] = 0
        result['risk_desc'] = '系统用户数量处于正常状态。'
        result['solution'] = '无'

    os.remove("passwd.txt")


if __name__ == '__main__':
    _result = {}
    process(_result)

    print(_result)
