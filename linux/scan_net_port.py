# Python 局域网扫描存活主机开放端口 
# 1、ping指定IP判断主机是否存活
# 2、ping所有IP获取所有存活主机
# 3、nmap扫描存活主机开放端口
# #注: 若在Linux系统下 ping -n 改为 ping -c
#      若在windows系统下 ping -n 不变

import os
import threading
import time

import nmap

IPList = []


def ping_ip(ip):  # 1、ping指定IP判断主机是否存活
    output = os.popen('ping -c 1 %s' % ip).readlines()  # 注：若在Linux系统下-n 改为 -c
    for w in output:
        if str(w).upper().find('TTL') >= 0:
            IPList.append(ip)


def ping_net(ip):  # 2、ping所有IP获取所有存活主机
    pre_ip = (ip.split('.')[:-1])
    for i in range(1, 256):
        add = ('.'.join(pre_ip) + '.' + str(i))
        threading._start_new_thread(ping_ip, (add,))
        time.sleep(0.01)


def nmapScan(ip):  # 3、nmap扫描存活主机开放端口
    findportcount = 0
    nmScan = nmap.PortScanner()
    x = nmScan.scan(ip)
    for port in range(1, 65536):
        try:
            state = x['scan'][ip]['tcp'][int(port)]['state']
            if state != 'unknown':
                print(ip, port, state)
                findportcount += 1
        except:
            pass
    # print('描述到端口数量：', findportcount)
    # if findportcount > 3:
    #     print('系统开放了太多端口，存在安全风险')



def process(result):
    # info = {}
    info = []
    result['info'] = info
    result['risk_level'] = 0
    result['risk_desc'] = '未发现网络端口问题。'
    result['solution'] = '无'

    findportcount = 0
    ip = "127.0.0.1"
    nmScan = nmap.PortScanner()
    x = nmScan.scan(ip)
    for port in range(1, 65536):
        try:
            state = x['scan'][ip]['tcp'][int(port)]['state']
            if state != 'unknown':
                # print(ip, port, state)
                findportcount += 1
                # info.append(port)
                # info.append(ip+port+state)

                port_info = {
                    'local_ip': ip,
                    'port': port,
                    'status': state,
                }
                info.append(port_info)

        except:
            pass

    # print('描述到端口数量：', findportcount)
    # if findportcount > 3:
    #     print('系统开放了太多端口，存在安全风险')

    # 开放端口大于3时，需检查确认是否有多余端口
    if findportcount > 3:
        result['risk_level'] = 1
        result['risk_desc'] = '系统开放了太多端口，存在安全风险 共计{}个端口。'.format(findportcount)
        result['solution'] = '请联系系统管理员，使用超级用户登录系统，维护等工作无关的端口'
    else:
        result['risk_level'] = 0
        result['risk_desc'] = '开放端口处于正常状态。'
        result['solution'] = '无'




if __name__ == '__main__':
    _result = {}
    process(_result)

    print(_result)

    # ping_net(socket.gethostbyname(socket.gethostname()))
    # for ip in IPList:
    #    nmapScan(ip)
    # nmapScan("127.0.0.1")
