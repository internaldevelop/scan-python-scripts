#!/bin/bash

echo "         (__)"

echo "         (oo)"

echo "   /------\/ "

echo "  / |    ||  "

echo " *  /\---/\  "

echo "   ~~   ~~   "

echo "...."Are You Ready?"..."

read key

echo "���棺���ű�ֻ��һ�����Ĳ�����δ�Է��������κ��޸ģ�����Ա���Ը��ݴ˱��������Ӧ�����á�"

echo ---------------------------------------������ȫ���-----------------------

echo "ϵͳ�汾"

uname -a

echo --------------------------------------------------------------------------

echo "������ip��ַ�ǣ�"

ifconfig | grep --color "\([0-9]\{1,3\}\.\)\{3\}[0-9]\{1,3\}"

echo --------------------------------------------------------------------------

awk -F":" '{if($2!~/^!|^*/){print "("$1")" " ��һ��δ���������˻��������Ա����Ƿ���Ҫ����������ɾ������"}}' /etc/shadow

echo --------------------------------------------------------------------------

more /etc/login.defs | grep -E "PASS_MAX_DAYS" | grep -v "#" |awk -F' '  '{if($2!=90){print "/etc/login.defs�����"$1 "���õ���"$2"�죬�����Ա�ĳ�90�졣"}}'

echo --------------------------------------------------------------------------

more /etc/login.defs | grep -E "PASS_MIN_LEN" | grep -v "#" |awk -F' '  '{if($2!=6){print "/etc/login.defs�����"$1 "���õ���"$2"���ַ��������Ա�ĳ�6���ַ���"}}'

echo --------------------------------------------------------------------------

more /etc/login.defs | grep -E "PASS_WARN_AGE" | grep -v "#" |awk -F' '  '{if($2!=10){print "/etc/login.defs�����"$1 "���õ���"$2"�죬�����Ա������ھ��������ĳ�10�졣"}}'

echo --------------------------------------------------------------------------

grep TMOUT /etc/profile /etc/bashrc > /dev/null|| echo "δ���õ�¼��ʱ���ƣ�������֮�����÷�������/etc/profile����/etc/bashrc�������TMOUT=600����"

echo --------------------------------------------------------------------------

if ps -elf |grep xinet |grep -v "grep xinet";then

echo "xinetd �����������У������Ƿ���԰�xinnetd����ر�"

else

echo "xinetd ����δ����"

fi

echo --------------------------------------------------------------------------

echo "�鿴ϵͳ�����ļ��޸�ʱ��"

ls -ltr /etc/passwd

echo --------------------------------------------------------------------------

echo  "�鿴�Ƿ�����ssh����"

if service sshd status | grep -E "listening on|active \(running\)"; then

echo "SSH�����ѿ���"

else

echo "SSH����δ����"

fi

echo --------------------------------------------------------------------------

echo "�鿴�Ƿ�����TELNET����"

if more /etc/xinetd.d/telnetd 2>&1|grep -E "disable=no"; then

echo  "TELNET�����ѿ��� "

else

echo  "TELNET����δ���� "

fi

echo --------------------------------------------------------------------------

echo  "�鿴ϵͳSSHԶ�̷������ò���(host.deny�ܾ��б�)"

if more /etc/hosts.deny | grep -E "sshd: ";more /etc/hosts.deny | grep -E "sshd"; then

echo  "Զ�̷��ʲ��������� "

else

echo  "Զ�̷��ʲ���δ���� "

fi

echo --------------------------------------------------------------------------

echo  "�鿴ϵͳSSHԶ�̷������ò���(hosts.allow�����б�)"

if more /etc/hosts.allow | grep -E "sshd: ";more /etc/hosts.allow | grep -E "sshd"; then

echo  "Զ�̷��ʲ��������� "

else

echo  "Զ�̷��ʲ���δ���� "

fi

echo "��hosts.allow�� host.deny���ͻʱ����hosts.allow����Ϊ׼��"

echo -------------------------------------------------------------------------

echo "�鿴shell�Ƿ����ó�ʱ��������"

if more /etc/profile | grep -E "TIMEOUT= "; then

echo  "ϵͳ�����˳�ʱ�������� "

else

echo  "δ���ó�ʱ�������� "

fi

echo -------------------------------------------------------------------------

echo "�鿴syslog��־��Ʒ����Ƿ���"

if service syslog status | egrep " active \(running";then

echo "syslog�����ѿ���"

else

echo "syslog����δ����������ͨ��service syslog start������־��ƹ���"

fi

echo -------------------------------------------------------------------------

echo "�鿴syslog��־�Ƿ����ⷢ"

if more /etc/rsyslog.conf | egrep "@...\.|@..\.|@.\.|\*.\* @...\.|\*\.\* @..\.|\*\.\* @.\.";then

echo "�ͻ���syslog��־�ѿ����ⷢ"

else

echo "�ͻ���syslog��־δ�����ⷢ"

fi

echo -------------------------------------------------------------------------

echo "�鿴passwd�ļ�������Щ��Ȩ�û�"

awk -F: '$3==0 {print $1}' /etc/passwd

echo ------------------------------------------------------------------------

echo "�鿴ϵͳ���Ƿ���ڿտ����˻�"

awk -F: '($2=="!!") {print $1}' /etc/shadow

echo "�ý����������Ubuntuϵͳ"

echo ------------------------------------------------------------------------

echo "�鿴ϵͳ��root�û��������"

lsof -u root |egrep "ESTABLISHED|SYN_SENT|LISTENING"

echo ----------------------------״̬����------------------------------

echo "ESTABLISHED����˼�ǽ������ӡ���ʾ��̨��������ͨ�š�"

echo "LISTENING��"

echo "SYN_SENT״̬��ʾ��������"

echo ------------------------------------------------------------------------

echo "�鿴ϵͳ��root�û�TCP�������"

lsof -u root |egrep "TCP"

echo ------------------------------------------------------------------------

echo "�鿴ϵͳ�д�����Щ��ϵͳĬ���û�"

echo "root:x:����ֵ����500Ϊ�´����û���С�ڻ����500Ϊϵͳ��ʼ�û���"

more /etc/passwd |awk -F ":" '{if($3>500){print "/etc/passwd�����"$1 "��ֵΪ"$3"�������Աȷ�ϸ��˻��Ƿ�������"}}'

echo ------------------------------------------------------------------------

echo "���ϵͳ�ػ�����"

more /etc/xinetd.d/rsync | grep -v "^#"

echo ------------------------------------------------------------------------

echo "���ϵͳ�Ƿ����������Ϊ"

more /var/log/secure |grep refused

echo ------------------------------------------------------------------------

echo "-----------------------���ϵͳ�Ƿ����PHP�ű�����---------------------"

if find / -type f -name *.php | xargs egrep -l "mysql_query\($query, $dbconn\)|ר������|udf.dll|class PHPzip\{|ZIPѹ������ ��Ұ�޵��޸İ�|$writabledb|AnonymousUserName|eval\(|Root_CSS\(\)|����PHPľ��|eval\(gzuncompress\(base64_decode|if\(empty\($_SESSION|$shellname|$work_dir |PHPľ��|Array\("$filename"| eval\($_POST\[|class packdir|disk_total_space|wscript.shell|cmd.exe|shell.application|documents and settings|system32|serv-u|��Ȩ|phpspy|����" |sort -n|uniq -c |sort -rn 1>/dev/null 2>&1;then

echo "��⵽PHP�ű�����"

find / -type f -name *.php | xargs egrep -l "mysql_query\($query, $dbconn\)|ר������|udf.dll|class PHPzip\{|ZIPѹ������ ��Ұ�޵��޸İ�|$writabledb|AnonymousUserName|eval\(|Root_CSS\(\)|����PHPľ��|eval\(gzuncompress\(base64_decode|if\(empty\($_SESSION|$shellname|$work_dir |PHPľ��|Array\("$filename"| eval\($_POST\[|class packdir|disk_total_space|wscript.shell|cmd.exe|shell.application|documents and settings|system32|serv-u|��Ȩ|phpspy|����" |sort -n|uniq -c |sort -rn

find / -type f -name *.php | xargs egrep -l "mysql_query\($query, $dbconn\)|ר������|udf.dll|class PHPzip\{|ZIPѹ������ ��Ұ�޵��޸İ�|$writabledb|AnonymousUserName|eval\(|Root_CSS\(\)|����PHPľ��|eval\(gzuncompress\(base64_decode|if\(empty\($_SESSION|$shellname|$work_dir |PHPľ��|Array\("$filename"| eval\($_POST\[|class packdir|disk_total_space|wscript.shell|cmd.exe|shell.application|documents and settings|system32|serv-u|��Ȩ|phpspy|����" |sort -n|uniq -c |sort -rn |awk '{print $2}' | xargs -I{} cp {} /tmp/

echo "���������ѿ�����/tmp/Ŀ¼"

else

echo "δ��⵽PHP�ű�����"

fi

echo ------------------------------------------------------------------------

echo "-----------------------���ϵͳ�Ƿ����JSP�ű�����---------------------"

find / -type f -name *.jsp | xargs egrep -l "InputStreamReader\(this.is\)|W_SESSION_ATTRIBUTE|strFileManag|getHostAddress|wscript.shell|gethostbyname|cmd.exe|documents and settings|system32|serv-u|��Ȩ|jspspy|����" |sort -n|uniq -c |sort -rn 2>&1

find / -type f -name *.jsp | xargs egrep -l "InputStreamReader\(this.is\)|W_SESSION_ATTRIBUTE|strFileManag|getHostAddress|wscript.shell|gethostbyname|cmd.exe|documents and settings|system32|serv-u|��Ȩ|jspspy|����" |sort -n|uniq -c |sort -rn| awk '{print $2}' | xargs -I{} cp {} /tmp/  2>&1 

echo ------------------------------------------------------------------------

echo "----------------------���ϵͳ�Ƿ����HTML�������---------------------"

if find / -type f -name *.html | xargs egrep -l "WriteData|svchost.exe|DropPath|wsh.Run|WindowBomb|a1.createInstance|CurrentVersion|myEncString|DropFileName|a = prototype;|204.351.440.495.232.315.444.550.64.330" 1>/dev/null 2>&1;then

echo "����HTML�������"

find / -type f -name *.html | xargs egrep -l "WriteData|svchost.exe|DropPath|wsh.Run|WindowBomb|a1.createInstance|CurrentVersion|myEncString|DropFileName|a = prototype;|204.351.440.495.232.315.444.550.64.330" |sort -n|uniq -c |sort -rn

find / -type f -name *.html | xargs egrep -l "WriteData|svchost.exe|DropPath|wsh.Run|WindowBomb|a1.createInstance|CurrentVersion|myEncString|DropFileName|a = prototype;|204.351.440.495.232.315.444.550.64.330" |sort -n|uniq -c |sort -rn| awk '{print $2}' | xargs -I{} cp {} /tmp/

echo "���������ѿ�����/tmp/Ŀ¼"

else

echo "δ��⵽HTML�������"

fi

echo "----------------------���ϵͳ�Ƿ����perl�������----------------------"

if find / -type f -name *.pl | xargs egrep -l "SHELLPASSWORD|shcmd|backdoor|setsockopt|IO::Socket::INET;" 1>/dev/null 2>&1;then

echo "����perl�������"

find / -type f -name *.pl | xargs egrep -l "SHELLPASSWORD|shcmd|backdoor|setsockopt|IO::Socket::INET;"|sort -n|uniq -c |sort -rn

find / -type f -name *.pl | xargs egrep -l "SHELLPASSWORD|shcmd|backdoor|setsockopt|IO::Socket::INET;"|sort -n|uniq -c |sort -rn| awk '{print $2}' | xargs -I{} cp {} /tmp/

echo "���������ѿ�����/tmp/Ŀ¼"

else

echo "δ��⵽perl�������"

fi

echo "----------------------���ϵͳ�Ƿ����Python�������----------------------"

find / -type f -name *.py | xargs egrep -l "execCmd|cat /etc/issue|getAppProc|exploitdb" |sort -n|uniq -c |sort -rn

find / -type f -name *.py | xargs egrep -l "execCmd|cat /etc/issue|getAppProc|exploitdb" |sort -n|uniq -c |sort -rn| awk '{print $2}' | xargs -I{} cp {} /tmp/

echo ------------------------------------------------------------------------

echo "-----------------------���ϵͳ�Ƿ���ڶ������---------------------"

find / -type f -perm -111  |xargs egrep "UpdateProcessER12CUpdateGatesE6C|CmdMsg\.cpp|MiniHttpHelper.cpp|y4'r3 1uCky k1d\!|execve@@GLIBC_2.0|initfini.c|ptmalloc_unlock_all2|_IO_wide_data_2|system@@GLIBC_2.0|socket@@GLIBC_2.0|gettimeofday@@GLIBC_2.0|execl@@GLIBC_2.2.5|WwW.SoQoR.NeT|2.6.17-2.6.24.1.c|Local Root Exploit|close@@GLIBC_2.0|syscall\(\__NR\_vmsplice,|Linux vmsplice Local Root Exploit|It looks like the exploit failed|getting root shell" 2>/dev/null

echo ------------------------------------------------------------------------

echo "����������Ӻͼ����˿�"

netstat -an 

echo "--------------------------·�ɱ��������ӡ��ӿ���Ϣ--------------"

netstat -rn 

echo "------------------------�鿴������ϸ��Ϣ--------------------------"

ifconfig -a 

echo ------------------------------------------------------------------------

echo "�鿴��������µ�¼�������������û�����ʷ��¼"

last

echo ------------------------------------------------------------------------

echo "���ϵͳ��core�ļ��Ƿ���"

ulimit -c

echo "core��unixϵͳ���ںˡ�����ĳ�������ڴ�Խ���ʱ��,����ϵͳ����ֹ��Ľ���,������ǰ�ڴ�״̬������core�ļ���,�Ա��һ��������������ؽ��Ϊ0�����ǹر��˴˹��ܣ�ϵͳ��������core�ļ�"

echo ------------------------------------------------------------------------

echo "���ϵͳ�йؼ��ļ��޸�ʱ��"

ls -ltr /bin/ls /bin/login /etc/passwd /bin/ps /usr/bin/top /etc/shadow|awk '{print "�ļ�����"$8"  ""����޸�ʱ�䣺"$6" "$7}'

echo "ls�ļ����Ǵ洢ls����Ĺ��ܺ�������ɾ���Ժ󣬾��޷�ִ��ls����ڿͿ����ô۸�ls�ļ���ִ�к��Ż���������

login�ļ���login�ǿ����û���¼���ļ���һ�����۸Ļ�ɾ����ϵͳ���޷��л��û����½�û�

user/bin/passwd��һ���������Ϊ�û���ӡ��������룬���ǣ��û������벢��������/etc/passwd���У����Ǳ�������/etc/shadow����

etc/passwd��һ���ļ�����Ҫ�Ǳ����û���Ϣ��

sbin/portmap���ļ�ת������ȱ�ٸ��ļ����޷�ʹ�ô��̹��ء�ת�����͵ȹ��ܡ�

bin/ps ���̲鿴�����֧���ļ����ļ��𻵻򱻸��ĺ��޷�����ʹ��ps���

usr/bin/top  top����֧���ļ�����Linux�³��õ����ܷ�������,�ܹ�ʵʱ��ʾϵͳ�и������̵���Դռ��״����

etc/shadow shadow �� /etc/passwd ��Ӱ���ļ����������ڸ��ļ����У�����ֻ��root�û��ɶ���"

echo --------------------------------------------------------------------------

echo "-------------------�鿴ϵͳ��־�ļ��Ƿ����--------------------"

log=/var/log/syslog

log2=/var/log/messages

if [ -e "$log" ]; then

echo  "syslog��־�ļ����ڣ� "

else

echo  "/var/log/syslog��־�ļ������ڣ� "

fi

if [ -e "$log2" ]; then

echo  "/var/log/messages��־�ļ����ڣ� "

else

echo  "/var/log/messages��־�ļ������ڣ� "

fi

echo --------------------------------------------------------------------------

echo "���ϵͳ�ļ�������2(MD5���)"

echo "������ȡ���ֹؼ��ļ���MD5ֵ����⣬Ĭ�ϱ�����/etc/md5db��"

echo "�����һ��ִ�У������ʾmd5sum: /sbin/portmap: û���Ǹ��ļ���Ŀ¼"

echo "�ڶ����ظ����ʱ������MD5DB�е�MD5ֵ����ƥ�䣬���ж��ļ��Ƿ񱻸��Ĺ�"

file="/etc/md5db"

if [ -e "$file" ]; then md5sum -c /etc/md5db 2>&1; 

else 

md5sum /etc/passwd >>/etc/md5db

md5sum /etc/shadow >>/etc/md5db

md5sum /etc/group >>/etc/md5db

md5sum /usr/bin/passwd >>/etc/md5db

md5sum /sbin/portmap>>/etc/md5db

md5sum /bin/login >>/etc/md5db

md5sum /bin/ls >>/etc/md5db

md5sum /bin/ps >>/etc/md5db

md5sum /usr/bin/top >>/etc/md5db;

fi

echo ----------------------------------------------------------------------

echo "------------------------�������ܼ��--------------------------------"

echo "CPU���"

dmesg | grep -i cpu

echo -----------------------------------------------------------------------

more /proc/cpuinfo

echo -----------------------------------------------------------------------

echo "�ڴ�״̬���"

vmstat 2 5

echo -----------------------------------------------------------------------

more /proc/meminfo

echo -----------------------------------------------------------------------

free -m

echo -----------------------------------------------------------------------

echo "�ļ�ϵͳʹ�����"

df -h

echo -----------------------------------------------------------------------

echo "����ʹ�����"

lspci -tv

echo ----------------------------------------------------------------------

echo "�鿴��ʬ����"

ps -ef | grep zombie

echo ----------------------------------------------------------------------

echo "��CPU���Ľ���"

ps auxf |sort -nr -k 3 |head -5

echo ----------------------------------------------------------------------

echo "���ڴ����Ľ���"

ps auxf |sort -nr -k 4 |head -5

echo ----------------------------------------------------------------------

echo ---------------------------------------------------------------------

echo "COPY RIGHT  �������"

echo "QQ��183126820"

echo ---------------------------------------------------------------------