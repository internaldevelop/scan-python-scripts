import os
import platform
# import json
import re


# 判断两个字符串版本号大小 例如：1.9 < 1.10<1.10.1
def compare(a, b):
    la = a.split('.')
    lb = b.split('.')
    f = 0
    if len(la) > len(lb):
        f = len(la)
    else:
        f = len(lb)
    for i in range(f):
        try:
            if int(la[i]) > int(lb[i]):
                print(a + '>' + b)
                return 1
            elif int(la[i]) == int(lb[i]):
                continue
            else:
                print(a + '<' + b)
                return 0
        except IndexError as e:
            if len(la) > len(lb):
                print(a + '>' + b)
                return 1
            else:
                print(a + '<' + b)
                return 0
    print(a + '=' + b)


# 获取操作系统版本信息
def show_os_all_info():
    '''打印os的全部信息'''
    print('获取操作系统名称及版本号 : [{}]'.format(platform.platform()))
    print('获取操作系统名称及版本号 : [{}]'.format(platform.platform(aliased=True)))
    print('获取操作系统名称及版本号 : [{}]'.format(platform.platform(terse=True)))
    print('获取操作系统版本号 : [{}]'.format(platform.version()))
    print('获取操作系统的位数 : [{}]'.format(platform.architecture()))
    print('计算机类型 : [{}]'.format(platform.machine()))
    print('计算机的网络名称 : [{}]'.format(platform.node()))
    print('计算机处理器信息 : [{}]'.format(platform.processor()))
    print('获取操作系统类型 : [{}]'.format(platform.system()))
    print('汇总信息 : [{}]'.format(platform.uname()))
    print('汇总信息 : [{}]'.format(platform.uname()._asdict()))


def process(result):
    info = {}
    result['info'] = info

    # show_os_all_info()

    version = platform.platform()
    print('version:',version)

    # re.sub(pattern, repl, string, count=0)
    # 参数说明：
    # pattern：正则重的模式字符串
    # repl：被拿来替换的字符串
    # string：要被用于替换的原始字符串
    # count：模式匹配后替换的最大次数，省略则默认为0，表示替换所有的匹配
    version = re.sub("[A-Za-z-_\!\%\[\]\,\。]", "", version)
    print('version:',version)

    #对比基准版本，根据版本号判断系统是否有安全更新
    iret = compare(version,"2.26")
    print('iret:',iret)
    if iret > 0:
        info['version'] = platform.platform()
        result['risk_level'] = 0
        result['risk_desc'] = '当前系统补丁包较新，无安全风险'
        result['solution'] = '无'

    else:
        info['version'] = platform.platform()
        result['risk_level'] = 1
        result['risk_desc'] = '当前系统补丁包版本过低，存在安全风险'
        result['solution'] = '联系管理员升级您的操作系统 参考命令：yum clean all & yum update'


if __name__ == '__main__':
    _result = {}
    process(_result)

    print(_result)
