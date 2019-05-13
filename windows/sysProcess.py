#!/usr/bin/python3.7
# coding=utf-8
import os
import sys

def getValue(t):
    try:
        return t[t.index(':') + 1:].strip()
    except:
        return ''


def getSCValue(line):
    try:
        return line[3].split(":")[1].strip()
    except:
        return 'Not Installed'


def process(result):
    output = os.system("systeminfo >system_info.log")
    lineArray = open("system_info.log", "r").readlines()

    result["OS Host Name"] = getValue(lineArray[1])
    result["OS Name"] = getValue(lineArray[2])
    result["OS Version"] = getValue(lineArray[3])
    result["OS Manufacturer"] = getValue(lineArray[4])
    result["OS Configuration"] = getValue(lineArray[5])
    result["OS Build Type"] = getValue(lineArray[6])
    result["OS Registered Owner"] = getValue(lineArray[7])
    result["OS Registered Organization"] = getValue(lineArray[8])
    result["OS Product ID"] = getValue(lineArray[9])
    result["OS Original Install Date"] = getValue(lineArray[10])
    result["System Boot Time"] = getValue(lineArray[11])
    result["System Manufacturer"] = getValue(lineArray[12])
    result["System Model"] = getValue(lineArray[13])
    result["System Type"] = getValue(lineArray[14])

    lineNum = 16
    for i in range(lineNum, len(lineArray)):
        if lineArray[i][0] != ' ':
            lineNum = i
            break
    result["System Processor(s)"] = [i.strip() for i in lineArray[16:lineNum]]

    result["System BIOS Version"] = getValue(lineArray[lineNum])
    lineNum = lineNum + 1

    result["OS Windows Directory"] = getValue(lineArray[lineNum])
    lineNum = lineNum + 1

    result["System Directory"] = getValue(lineArray[lineNum])
    lineNum = lineNum + 1

    result["System Boot Device"] = getValue(lineArray[lineNum])
    lineNum = lineNum + 1

    result["OS Locale"] = getValue(lineArray[lineNum])
    lineNum = lineNum + 1

    result["OS Input Locale"] = getValue(lineArray[lineNum])
    lineNum = lineNum + 1

    result["OS Time Zone"] = getValue(lineArray[lineNum])
    lineNum = lineNum + 1

    result["System Total Physical Memory"] = getValue(lineArray[lineNum])
    lineNum = lineNum + 1

    result["System Available Physical Memory"] = getValue(lineArray[lineNum])
    lineNum = lineNum + 1

    result["OS Virtual Memory: Max Size"] = getValue(lineArray[lineNum])
    lineNum = lineNum + 1

    result["OS Virtual Memory: Available"] = getValue(lineArray[lineNum])
    lineNum = lineNum + 1

    result["OS Virtual Memory: In Use"] = getValue(lineArray[lineNum])
    lineNum = lineNum + 1

    result["OS Page File Location(s)"] = getValue(lineArray[lineNum])
    lineNum = lineNum + 1

    result["OS Domain"] = getValue(lineArray[lineNum])
    lineNum = lineNum + 1

    result["OS Logon Server"] = getValue(lineArray[lineNum])

    lineNum = lineNum + 2

    for i in range(lineNum, len(lineArray)):
        if lineArray[i][0] != ' ':
            endNum = i
            break
    result["OS Hotfix(s)"] = [i.strip() for i in lineArray[lineNum:endNum]]

    output = os.system("sc query wscsvc >system_Alerter.log")
    result['System Alerter'] = getSCValue(open("system_Alerter.log", 'r').readlines())

    output = os.system("sc query wuauserv >system_autoupdate.log")
    result['System Autoupdate'] = getSCValue(open("system_autoupdate.log", 'r').readlines())

    os.remove('system_info.log')
    os.remove('system_Alerter.log')
    os.remove('system_autoupdate.log')

    return


if __name__ == '__main__':
    r = {}
    process(r)
    print(r)
