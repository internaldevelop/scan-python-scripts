#!/usr/bin/python3.7
# coding=utf-8
import psutil
# from json import JSONEncoder
import json


def process(result):
    info = {}
    result['info'] = info

    # 获取所有磁盘的分区信息
    disk_part = psutil.disk_partitions()

    # 系统磁盘的分区信息，named-tuple 通过 _asdict 转换成 dict 对象
    sys_disk_part = disk_part[0]._asdict()
    # info['System Disk Partition'] = JSONEncoder().encode(sys_disk_part)
    info['System Disk Partition'] = json.dumps(sys_disk_part)
    # sys_disk_part_dict = sys_disk_part._asdict()
    if sys_disk_part['device'] != 'C:\\':
        result['risk_level'] = 3
        result['risk_desc'] = '未成功获取磁盘分区信息。'
        result['solution'] = '请检查磁盘分区信息，确保系统盘的正确分区。'
    elif sys_disk_part['fstype'] != 'NTFS':
        result['risk_level'] = 2
        result['risk_desc'] = '系统盘没有采用NTFS文件系统，不支持文件安全设置。'
        result['solution'] = '为保证文件系统的安全性，建议将磁盘改成NTFS文件系统，并重新安装操作系统。'
    else:
        result['risk_level'] = 0
        result['risk_desc'] = '系统盘采用了NTFS文件系统，支持文件安全设置。'
        result['solution'] = '无。'

    return


if __name__ == '__main__':
    _result = {}
    process(_result)

    print(_result)
