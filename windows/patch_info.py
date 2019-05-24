#!/usr/bin/python3.7
# coding=utf-8
import os
import re
# import sys


def getValue(t):
    try:
        return t[t.index(':') + 1:].strip()
    except ValueError:
        return ''


def noPatch(result):
    result['info'] = '补丁列表：\n[ 空 ]'
    result['risk_level'] = 3
    result['risk_desc'] = '未安装系统补丁，有较严重的安全隐患'
    result['solution'] = '配置Windows Update，连接互联网，更新系统修补程序。'

    return


def process(result):
    output = os.system("systeminfo >system_info.log")
    line_array = open("system_info.log", "r").readlines()

    line_index = 33

    # end_index = start_index
    if line_array[line_index].find('暂缺') >= 0:
        noPatch(result)
    else:
        match_obj = re.findall(r"\d+\.?\d*", line_array[line_index])
        if len(match_obj) == 0:
            noPatch(result)
        else:
            patch_count = int(match_obj[0])
            result['info'] = '补丁列表(' + str(patch_count) + '个)：\n'
            for index in range(line_index + 1, len(line_array)):
                if line_array[index].find(']: KB') < 0:
                    break
                result['info'] += line_array[index]
            if 0 < patch_count < 10:
                result['risk_level'] = 1
                result['risk_desc'] = '系统补丁过少，存在安全风险'
                result['solution'] = '配置Windows Update，连接互联网，更新系统修补程序。'
            else:
                # TODO: 添加检查最新补丁
                result['risk_level'] = 0
                result['risk_desc'] = '补丁安装正常'
                result['solution'] = '无'

    os.remove('system_info.log')

    return


if __name__ == '__main__':
    r = {}
    process(r)
    print(r)
