#!/usr/bin/python3.7
# coding=utf-8
import os


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
    line = open("system_info.log", "r").readlines()

    result["OS Host Name"] = getValue(line[1])
    result["OS Name"] = getValue(line[2])
    result["OS Version"] = getValue(line[3])
    result["OS Manufacturer"] = getValue(line[4])
    result["OS Configuration"] = getValue(line[5])
    result["OS Build Type"] = getValue(line[6])
    result["OS Registered Owner"] = getValue(line[7])
    result["OS Registered Organization"] = getValue(line[8])
    result["OS Product ID"] = getValue(line[9])
    result["OS Original Install Date"] = getValue(line[10])
    result["System Boot Time"] = getValue(line[11])
    result["System Manufacturer"] = getValue(line[12])
    result["System Model"] = getValue(line[13])
    result["System Type"] = getValue(line[14])

    lineNum = 16
    for i in range(lineNum, len(line)):
        if line[i][0] != ' ':
            lineNum = i
            break
    result["System Processor(s)"] = [i.strip() for i in line[16:lineNum]]

    result["System BIOS Version"] = getValue(line[lineNum])
    lineNum = lineNum + 1

    result["OS Windows Directory"] = getValue(line[lineNum])
    lineNum = lineNum + 1

    result["System Directory"] = getValue(line[lineNum])
    lineNum = lineNum + 1

    result["System Boot Device"] = getValue(line[lineNum])
    lineNum = lineNum + 1

    result["OS Locale"] = getValue(line[lineNum])
    lineNum = lineNum + 1

    result["OS Input Locale"] = getValue(line[lineNum])
    lineNum = lineNum + 1

    result["OS Time Zone"] = getValue(line[lineNum])
    lineNum = lineNum + 1

    result["System Total Physical Memory"] = getValue(line[lineNum])
    lineNum = lineNum + 1

    result["System Available Physical Memory"] = getValue(line[lineNum])
    lineNum = lineNum + 1

    result["OS Virtual Memory: Max Size"] = getValue(line[lineNum])
    lineNum = lineNum + 1

    result["OS Virtual Memory: Available"] = getValue(line[lineNum])
    lineNum = lineNum + 1

    result["OS Virtual Memory: In Use"] = getValue(line[lineNum])
    lineNum = lineNum + 1

    result["OS Page File Location(s)"] = getValue(line[lineNum])
    lineNum = lineNum + 1

    result["OS Domain"] = getValue(line[lineNum])
    lineNum = lineNum + 1

    result["OS Logon Server"] = getValue(line[lineNum])

    lineNum = lineNum + 2

    for i in range(lineNum, len(line)):
        if line[i][0] != ' ':
            endNum = i
            break
    result["OS Hotfix(s)"] = [i.strip() for i in line[lineNum:endNum]]

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
