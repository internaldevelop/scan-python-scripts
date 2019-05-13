#!/usr/bin/python2.7
#coding=utf-8
import os

def getOneLine(ssh,cmd):
    try:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        output=stdout.readlines()
        if output:
        	return str(output[0])
        else:
        	return ''
    except:
        return ''


def getAllLine(ssh,cmd):
    try:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        output=stdout.readlines()
        #print (cmd,output,stderr.readlines())
        if output:
        	return list(output)
        else:
        	return []
    except:
        return []
   
def getUser2(ssh):
    print pwd
    try:
        stdin, stdout, stderr = ssh.exec_command('''awk -F":" '{if($2!~/^!|^*/){print $1 }}' /etc/shadow''')
        output=stdout.readlines()
        #print output
        return str(output)
    except:
        return []

def getUser(ssh):
    userList=[]
    try:
        stdin, stdout, stderr = ssh.exec_command('''cat  /etc/shadow''')
        output=stdout.readlines()
        for i in output:
            user,pwd,lastChangeTime,minTime,maxTime,warnTime,UnActiveTime,expiredTime,flag=str(i).split(':')
            #登录名:加密口令:最后一次修改时间:最小时间间隔:最大时间间隔:警告时间:不活动时间:失效时间:标志
            if pwd !='~' and pwd !='!!'  and pwd !='*' and pwd!='':
                #print user,pwd,lastChangeTime,minTime,maxTime,warnTime,UnActiveTime,expiredTime,flag
                userList+=[user]
        return userList
    except:
        return []

def getPwdTime(ssh,rDict):
    try:
        stdin, stdout, stderr = ssh.exec_command('''cat  /etc/login.defs''')
        output=stdout.readlines()
        for i in output:
            if "PASS_MAX_DAYS" in i:
                rDict['Linux PASS_MAX_DAYS']=i.split()[1]
            elif "PASS_MIN_DAYS" in i:
                rDict['Linux PASS_MIN_DAYS']=i.split()[1]
            elif "PASS_MIN_LEN" in i:
                rDict['Linux PASS_MIN_LEN']=i.split()[1]
            elif "PASS_WARN_AGE" in i:
                rDict['Linux PASS_WARN_AGE']=i.split()[1]

        return 
    except:
        return

def process(rDict):
    ssh=rDict['SSHObj']
    #ip=rDict['ip']


    rDict['Linux OS kernel-name']=getOneLine(ssh,'uname -s')
    rDict['Linux OS nodename']=getOneLine(ssh,'uname -n')
    rDict['Linux OS kernel-release']=getOneLine(ssh,'uname -r')
    rDict['Linux OS kernel-version']=getOneLine(ssh,'uname -v')
    rDict['Linux OS machine']=getOneLine(ssh,'uname -m')
    rDict['Linux OS processor']=getOneLine(ssh,'uname -p')
    rDict['Linux OS hardware-platform']=getOneLine(ssh,'uname -i')
    rDict['Linux OS operating-system']=getOneLine(ssh,'uname -o')
    
    version=getOneLine(ssh,'cat /proc/version')
    try:
        rDict['Linux OS kernel-compiler']=version.split()[3]
    except:
        print version
        rDict['Linux OS kernel-compiler']=version.split()
    #未锁定账户
    rDict['Linux Account Users']=getUser(ssh)

    
    getPwdTime(ssh,rDict)
    
    #"未设置登录超时限制，请设置之，设置方法：在/etc/profile或者/etc/bashrc里面添加TMOUT=600参数"
    rDict['Linux OS shell-TMOUT']=getOneLine(ssh,'cat /etc/profile | grep -E "TMOUT"')


    #"查看系统密码文件修改时间"
    rDict['Linux OS passwd-LS-ltr']=getOneLine(ssh,'ls -ltr /etc/passwd')


    
    #"查看系统SSH远程访问设置策略(host.deny拒绝列表)"
    rDict['Linux OS SSH-Deny']=getAllLine(ssh,"""cat /etc/hosts.deny | grep -E "sshd:" """)

    #"查看系统SSH远程访问设置策略(hosts.allow允许列表)"
    rDict['Linux OS SSH-Allow']=getAllLine(ssh,"""cat /etc/hosts.allow | grep -E "sshd:" """)

    #"查看syslog日志审计服务是否开启"
    rDict['Linux Log Active']=getAllLine(ssh,"""service rsyslog status | grep -E "running" """)

    #"检查系统守护进程"
    rDict['Linux OS rsync']=getAllLine(ssh,"""cat /etc/xinetd.d/rsync | grep -v "^#" """)

    #"检查系统是否存在入侵行为"
    rDict['Linux Log secure']=getAllLine(ssh,"""cat /var/log/secure | grep refused """)

    #"检查网络连接和监听端口"
    rDict['Linux Network Connection']=getAllLine(ssh,"""netstat -an """)

    #"检查路由表、网络连接、接口信息"
    rDict['Linux Network route']=getAllLine(ssh,"""netstat -rn """)
    rDict['Linux Last']=getAllLine(ssh,"""last""")

    #检查系统中core文件是否开启
    rDict['Linux Os Core']=getAllLine(ssh,"""ulimit -c""")

    #"检查系统中关键文件修改时间"
    rDict['Linux File CHange']=getAllLine(ssh,"""ls -ltr /bin/ls /bin/login /etc/passwd /bin/ps /usr/bin/top /etc/shadow | awk '{print $9",",$8,$6,$7}' """)
    
    #"文件系统使用情况"
    rDict['Linux File usage']=getAllLine(ssh,"""df -h """)

    #"检查系统中服务运行状态"
    rDict['Linux Service status']=getAllLine(ssh,"""service --status-all """)
 
    #"检查系统中补丁安装情况"
    rDict['Linux Service RPM']=getAllLine(ssh,"""rpm -qa --last """)

    #"检查系统中SSH安全配置"
    rDict['Linux Service SSH']=getAllLine(ssh,"""cat /etc/ssh/sshd_config""")

    #"检查系统中环境变量路径"
    rDict['Linux Service root path']=getAllLine(ssh,"""env""")

    #"检查系统中加载的内核模块"
    rDict['Linux Service mod']=getAllLine(ssh,"""lsmod """)

    #"检查系统防火墙配置"
    rDict['Linux Service firewall']=getAllLine(ssh,"""iptables -L""")

    #"检查系统中环境变量路径"
    #rDict['Service root path']=getAllLine(ssh,"""env""")



    return



if __name__ == '__main__':

    r={}
    process(r)
    print r
   
